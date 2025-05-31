from django.contrib import admin
from .models import ChatMessage  # import the correct model name

admin.site.register(ChatMessage)  # register the model
