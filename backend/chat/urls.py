from django.urls import path
from .views import chat_view, ChatMessageListCreateView, get_chat_history

urlpatterns = [
    path('', chat_view, name='chat'),  # Handles POST to initiate chat
    path('messages/', ChatMessageListCreateView.as_view(), name='chat-list-create'),  # List & create chat entries
    path('chat-history/<uuid:session_id>/', get_chat_history, name='chat-history'),  # Session-based chat history
]
