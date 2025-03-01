from django.db import models
from django.contrib.auth.models import User
from djongo import models as djongo_models
from django import forms

# We'll use Django's built-in User model for authentication

class ChatHistory(djongo_models.Model):
    """Model to store chat history for each user"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    input_text = models.TextField()
    output_text = models.TextField()
    operation_type = models.CharField(max_length=50)  # 'summarize', 'rewrite', etc.
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.operation_type} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
    
    class Meta:
        ordering = ['-timestamp']