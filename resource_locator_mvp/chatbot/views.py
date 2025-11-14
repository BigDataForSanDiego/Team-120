from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import google.generativeai as genai
from django.conf import settings

class ChatbotView(APIView):
    def post(self, request):
        import traceback
        user_query = request.data.get('userQuery')
        # language param: 'en' (English) or 'es' (Spanish). Default to 'en'.
        language = (request.data.get('language') or 'en').lower()
        if language not in ('en', 'es'):
            # accept common variants
            language = 'es' if language.startswith('es') else 'en'
        if not user_query:
            return Response({'error': 'No query provided'}, status=status.HTTP_400_BAD_REQUEST)

        # System prompt for Good Fellow
        system_prompt = """
        You are Good Fellow — an AI-powered bilingual (English and Spanish)
        community resource assistant for the San Diego area.
        Your mission is to connect users with verified, local community services (food, shelter, medical, job training).
        Always respond in the same language as the user (English or Spanish).
        Use a compassionate tone and accurate, local information.
        Focus strictly on San Diego County.
        """

        try:
            # Configure Google Generative AI
            genai.configure(api_key=settings.GOOGLE_API_KEY)
            # Preferred model for high-quality responses. Using an available model from the API list.
            # Chosen model (from server-provided available models): use a broadly-available flash model.
            requested_model = 'models/gemini-flash-latest'
            # Add explicit language instruction so the model responds in the requested language.
            # Also instruct the model to produce plain, human-readable text without markdown or special characters.
            lang_instruction = 'Respond in Spanish.' if language == 'es' else 'Respond in English.'
            format_instruction = (
                "Respond using plain, human-readable text only. Do NOT use Markdown, headings, triple-backticks, bold/italic markers, or bullet/list markers like '*' or numbered lists. "
                "Return normal sentences and short paragraphs; avoid any decorative characters (e.g., **, *, ###, ```)."
            )

            full_prompt = f"{system_prompt}\n\n{lang_instruction} {format_instruction}\n\nUser: {user_query}\n\nAI:"

            try:
                model = genai.GenerativeModel(requested_model)
                response = model.generate_content(full_prompt)
                response_text = response.text
                # Sanitize common Markdown-like artifacts just in case the model includes them.
                import re
                def clean_response(txt: str) -> str:
                    if not txt:
                        return txt
                    # Remove backticks and code fences
                    txt = re.sub(r'`{1,}', '', txt)
                    # Remove bold/italic markers (**, __, *, _ , ~~)
                    txt = re.sub(r"\*\*|__|~~", '', txt)
                    txt = re.sub(r"(?m)^\s*\*\s+", '', txt)  # lines starting with * bullets
                    txt = re.sub(r"(?m)^\s*[-+]\s+", '', txt)  # lines starting with - or + bullets
                    txt = re.sub(r"(?m)^\s*\d+\.\s+", '', txt)  # lines starting with numbered lists
                    # Remove leading heading markers
                    txt = re.sub(r"(?m)^\s*#{1,6}\s*", '', txt)
                    # Collapse excessive whitespace/newlines
                    txt = re.sub(r"\n{3,}", '\n\n', txt)
                    # Trim
                    return txt.strip()

                response_text = clean_response(response_text)
            except Exception as model_ex:
                # If the requested model isn't available for this API version, try to list available models
                try:
                    available = genai.list_models()
                    # Normalize to a list of names
                    names = []
                    for m in available:
                        if isinstance(m, dict):
                            name = m.get('name') or m.get('model') or str(m)
                        else:
                            name = getattr(m, 'name', None) or str(m)
                        names.append(name)
                    raise RuntimeError(
                        f"Requested model '{requested_model}' is not available for this API/version. "
                        f"Available models: {names}"
                    ) from model_ex
                except Exception as list_ex:
                    # If listing models also fails, surface both errors
                    raise RuntimeError(
                        f"Requested model '{requested_model}' unavailable; additionally failed to list models: {list_ex}"
                    ) from model_ex

            return Response({'response': response_text}, status=status.HTTP_200_OK)
        except Exception as e:
            traceback.print_exc()
            error_msg = str(e)
            print(f"Chatbot Error: {error_msg}")
            return Response({'error': error_msg}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
