from django.urls import path
from .views import ChatbotView

urlpatterns = [
    path('api/chat/', ChatbotView.as_view(), name='chatbot'),
    
]