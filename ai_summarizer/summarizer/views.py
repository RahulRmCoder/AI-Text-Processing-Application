from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import requests
import os
from .serializers import SummarizeSerializer, RewriteSerializer

# Load API Key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Add this new view for frontend
def frontend_view(request):
    """
    Render the frontend interface
    """
    return render(request, 'summarizer/index.html')

class SummarizeView(APIView):
    """
    View to summarize input text using Groq API
    """
    def post(self, request):
        serializer = SummarizeSerializer(data=request.data)
        if serializer.is_valid():
            input_text = serializer.validated_data['text']

            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            }

            data = {
                "model": "mixtral-8x7b-32768",
                "messages": [{"role": "user", "content": f"Summarize this: {input_text}"}],
                "temperature": 0.5
            }

            response = requests.post(GROQ_API_URL, json=data, headers=headers)

            if response.status_code == 200:
                result = response.json()
                summary = result.get("choices", [{}])[0].get("message", {}).get("content", "No response generated.")
                return Response({"summary": summary}, status=status.HTTP_200_OK)
            return Response({"error": "Failed to get summary"}, status=response.status_code)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RewriteView(APIView):
    """
    View to rewrite text in a specified style
    """
    def post(self, request):
        serializer = RewriteSerializer(data=request.data)
        if serializer.is_valid():
            input_text = serializer.validated_data['text']
            style = serializer.validated_data['style']

            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            }

            data = {
                "model": "mixtral-8x7b-32768",
                "messages": [{"role": "user", "content": f"Rewrite this in {style} style: {input_text}"}],
                "temperature": 0.7
            }

            response = requests.post(GROQ_API_URL, json=data, headers=headers)

            if response.status_code == 200:
                result = response.json()
                rewritten_text = result.get("choices", [{}])[0].get("message", {}).get("content", "No response generated.")
                return Response({"rewritten_text": rewritten_text}, status=status.HTTP_200_OK)
            return Response({"error": "Failed to rewrite text"}, status=response.status_code)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)