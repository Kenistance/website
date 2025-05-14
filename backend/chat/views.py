from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import ChatMessage
from .serializers import ChatMessageSerializer


# ChatMessageListCreateView: Used for listing and creating new chat messages
class ChatMessageListCreateView(generics.ListCreateAPIView):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer


# chat_view: Handle bot responses to user messages
@api_view(['POST'])
def chat_view(request):
    user_message = request.data.get("message", "").strip()

    if not user_message:
        return Response({"error": "Message is required."}, status=status.HTTP_400_BAD_REQUEST)

    message = user_message.lower()
    reply = "I'm not sure how to respond to that yet, but I'm learning!"

    # Expanded bot replies
    if "hello" in message or "hi" in message:
        reply = "Hi there! How can I help you today?"
    elif "services" in message:
        reply = "I offer automation, analytics, project work, and web development."
    elif "portfolio" in message:
        reply = "You can view my past projects in the Portfolio section of the site."
    elif "price" in message or "cost" in message:
        reply = "Prices vary based on the project. Can you describe what you need?"
    elif "contact" in message:
        reply = "You can contact me using the enquiry form or the chat box here!"
    elif "available" in message:
        reply = "I'm usually available on weekdays. Send a message to discuss timing."
    elif "time" in message:
        reply = "Turnaround time depends on the project. Small tasks can be done in a day or two."
    elif "automation" in message:
        reply = "I can help automate tasks using Python — like Excel, web scraping, and data workflows."
    elif "data" in message:
        reply = "I work with data using Python, pandas, and other tools. What’s your project?"
    elif "python" in message:
        reply = "Yes, I primarily code in Python for most backend, automation, and analytics tasks."
    elif "react" in message:
        reply = "Yes, I use React for frontend development along with Tailwind for styling."
    elif "django" in message:
        reply = "Absolutely — Django powers the backend of this very site!"
    elif "thanks" in message or "thank you" in message:
        reply = "You're very welcome! Let me know if you have more questions. 😊"
    elif "bye" in message or "goodbye" in message:
        reply = "Goodbye! Hope to hear from you again soon."
    elif "project" in message:
        reply = "I’d love to hear about your project! Could you share some details?"
    elif "custom" in message:
        reply = "Yes, I can build custom tools or dashboards. What do you need?"
    elif "booking" in message:
        reply = "You can book services through the booking page — or send a request here."
    elif "chat" in message:
        reply = "Yes, you can chat with me anytime here. I'm always ready to help!"
    elif "enquiry" in message:
        reply = "Use the enquiry box or the contact form to send a detailed message."
    elif "who are you" in message:
        reply = "I'm your assistant — here to help with your tech and project needs!"
    elif "help" in message:
        reply = "Sure, I'm here to help. What would you like to know more about?"

    # Save the chat
    chat_message = ChatMessage.objects.create(
        user_message=user_message,
        bot_reply=reply
    )

    serializer = ChatMessageSerializer(chat_message)
    return Response({
        "response": reply,
        "chat": serializer.data
    })
