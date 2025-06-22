from rest_framework import serializers
from .models import ChatHistory

class SummarizeSerializer(serializers.Serializer):
    text = serializers.CharField()

class RewriteSerializer(serializers.Serializer):
    text = serializers.CharField()
    style = serializers.ChoiceField(choices=['formal', 'casual', 'creative','academic','business'])

# Add a serializer for the ChatHistory model to use with API if needed
class ChatHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatHistory
        fields = ['id', 'input_text', 'output_text', 'operation_type', 'timestamp']
        read_only_fields = ['id', 'timestamp']
