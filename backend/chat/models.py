from django.db import models

class ChatMessage(models.Model):
    user_message = models.TextField()
    bot_reply = models.TextField(default="Default reply")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User: {self.user_message[:30]} | Bot: {self.bot_reply[:30]}"
