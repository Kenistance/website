# serializers.py
from rest_framework import serializers
from .models import ChatMessage

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['user_message', 'bot_reply', 'timestamp', 'session_id']
