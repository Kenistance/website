# chat/urls.py
from django.urls import path
from .views import chat_view, ChatMessageListCreateView

urlpatterns = [
    path('', chat_view, name='chat'),  # Just '' — not 'api/chat/'
    path('messages/', ChatMessageListCreateView.as_view(), name='chat-list-create'),
]
