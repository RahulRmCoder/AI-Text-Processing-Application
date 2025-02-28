from rest_framework import serializers

class SummarizeSerializer(serializers.Serializer):
    text = serializers.CharField()

class RewriteSerializer(serializers.Serializer):
    text = serializers.CharField()
    style = serializers.ChoiceField(choices=['formal', 'casual', 'creative'])
