from django.db import models
import uuid  # For generating UUIDs

class ChatMessage(models.Model):
    user_message = models.TextField()
    bot_reply = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    session_id = models.UUIDField(default=uuid.uuid4, editable=False)  # UUID for unique session tracking

    def __str__(self):
        return f"User: {self.user_message[:20]}... | Bot: {self.bot_reply[:20]}..."
