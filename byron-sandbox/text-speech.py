import os
import sys
import whisper
from pathlib import Path
from dotenv import load_dotenv 
from openai import OpenAI

import torch
from TTS.api import TTS

def speechToText(inputFile):
  model = whisper.load_model("turbo")
  result = model.transcribe(inputFile)
  resultFormatted = result["text"]
  print(resultFormatted)
  return resultFormatted
  

def textToSpeech(textToRead):
  # device = "cuda" if torch.cuda.is_available() else "cpu"

  # for model in TTS().list_models():
  #   print(model)

  tts = TTS("tts_models/en/ek1/tacotron2", progress_bar=True)
  tts.tts_to_file(text=textToRead, file_path="/Users/byronjtran/SDSU/Team-120/byron-sandbox/output.wav")
 



# this will be controlled elsewhere when implemented
inputFile = sys.argv[1]
transcript = speechToText(inputFile)

textToSpeech(transcript)