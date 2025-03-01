from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import requests
import os
from .models import ChatHistory
from .forms import SummarizerForm
from .serializers import SummarizeSerializer, RewriteSerializer, ChatHistorySerializer

# Load API Key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# User Authentication Views
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully.")
            return redirect('home')
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
    else:
        form = UserCreationForm()
    
    return render(request, 'summarizer/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'summarizer/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')

# Frontend view
def frontend_view(request):
    """
    Render the frontend interface
    """
    return render(request, 'summarizer/index.html')

# Web Interface Views
@login_required(login_url='login')
def home_view(request):
    if request.method == 'POST':
        form = SummarizerForm(request.POST)
        if form.is_valid():
            input_text = form.cleaned_data['input_text']
            operation = form.cleaned_data['operation']
            
            # Process text based on operation using Groq API
            if operation == 'summarize':
                output_text = call_groq_api(input_text, "summarize")
            elif operation == 'rewrite':
                style = form.cleaned_data.get('style', 'formal')  # Default to formal style
                output_text = call_groq_api(input_text, "rewrite", style=style)
            else:
                output_text = "Unknown operation"
            
            # Save to chat history
            ChatHistory.objects.create(
                user=request.user,
                input_text=input_text,
                output_text=output_text,
                operation_type=operation if operation == 'summarize' else f"rewrite_{style}"
            )
            
            context = {
                'form': form,
                'input_text': input_text,
                'output_text': output_text,
                'operation': operation
            }
            return render(request, 'summarizer/index.html', context)
    else:
        form = SummarizerForm()
    
    return render(request, 'summarizer/index.html', {'form': form})

@login_required(login_url='login')
def history_view(request):
    history = ChatHistory.objects.filter(user=request.user)
    return render(request, 'summarizer/history.html', {'history': history})

@login_required(login_url='login')
def clear_history(request):
    if request.method == 'POST':
        ChatHistory.objects.filter(user=request.user).delete()
        messages.success(request, "Chat history cleared successfully.")
    return redirect('history')

# API for history if needed
class UserHistoryView(APIView):
    """
    View to get user's chat history
    """
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)
        
        history = ChatHistory.objects.filter(user=request.user)
        serializer = ChatHistorySerializer(history, many=True)
        return Response(serializer.data)

# API Views
class SummarizeView(APIView):
    """
    View to summarize input text using Groq API
    """
    def post(self, request):
        serializer = SummarizeSerializer(data=request.data)
        if serializer.is_valid():
            input_text = serializer.validated_data['text']
            
            summary = call_groq_api(input_text, "summarize")
            
            # Save to history if user is authenticated
            if request.user.is_authenticated:
                ChatHistory.objects.create(
                    user=request.user,
                    input_text=input_text,
                    output_text=summary,
                    operation_type="summarize"
                )
                
            return Response({"summary": summary}, status=status.HTTP_200_OK)
        
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
            
            rewritten_text = call_groq_api(input_text, "rewrite", style=style)
            
            # Save to history if user is authenticated
            if request.user.is_authenticated:
                ChatHistory.objects.create(
                    user=request.user,
                    input_text=input_text,
                    output_text=rewritten_text,
                    operation_type=f"rewrite_{style}"
                )
                
            return Response({"rewritten_text": rewritten_text}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Helper function to call Groq API
def call_groq_api(text, operation_type, style=None):
    """
    Helper function to call Groq API for text processing
    """
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    if operation_type == "summarize":
        prompt = f"Summarize this: {text}"
    elif operation_type == "rewrite":
        prompt = f"Rewrite this in {style} style: {text}"
    else:
        return "Invalid operation type"
    
    data = {
        "model": "mixtral-8x7b-32768",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7 if operation_type == "rewrite" else 0.5
    }
    
    try:
        response = requests.post(GROQ_API_URL, json=data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            return result.get("choices", [{}])[0].get("message", {}).get("content", "No response generated.")
        return f"API Error: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"