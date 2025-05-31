from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ChatMessage
from .serializers import ChatMessageSerializer
from difflib import get_close_matches
import uuid
import re

# Enhanced in-memory session store with context tracking
session_context = {}

def fuzzy_match(phrase, keywords, cutoff=0.7):
    """Enhanced fuzzy matching that works with multi-word phrases too"""
    # Try exact matches first
    for keyword in keywords:
        if keyword in phrase.lower():
            return keyword
    
    # Try individual words in the phrase
    for word in phrase.lower().split():
        match = get_close_matches(word, keywords, n=1, cutoff=cutoff)
        if match:
            return match[0]
    
    return None

@api_view(['POST'])
def chat_view(request):
    user_message = request.data.get("message", "").strip()
    if not user_message:
        return Response({"error": "Message is required."}, status=status.HTTP_400_BAD_REQUEST)

    session_id = request.data.get("session_id") or str(uuid.uuid4())
    
    # Get or initialize session context
    if session_id not in session_context:
        session_context[session_id] = {
            "last_topic": None,
            "conversation_history": [],
            "follow_up_context": None,
            "awaiting_more_details": False
        }
    
    context = session_context[session_id]
    context["conversation_history"].append(user_message)
    
    # Track the full message and cleaned version for processing
    message = user_message.lower()
    
    # Handle various intents and responses
    reply = process_message(message, context)
    
    # Save chat to database
    chat_message = ChatMessage.objects.create(
        user_message=user_message,
        bot_reply=reply,
        session_id=session_id
    )
    serializer = ChatMessageSerializer(chat_message)

    return Response({
        "response": reply,
        "session_id": session_id,
        "chat": serializer.data
    }, status=status.HTTP_200_OK)

def process_message(message, context):
    """Process the user message with context awareness"""
    
    # Define all response categories
    greetings = ["hello", "hi", "hey", "good morning", "good evening", "good afternoon", "greetings"]
    thanks = ["thanks", "thank you", "thx", "appreciate", "grateful"]
    farewells = ["bye", "goodbye", "see you", "take care", "farewell"]
    
    # Industry-specific knowledge
    industries = {
        "health": {
            "general": "In healthcare, we help with patient dashboards, data analytics, appointment automation, and AI diagnostic tools.",
            "details": "We offer comprehensive healthcare solutions including:\n\nPatient Management Systems\nAI-driven diagnostic assistance tools\nMedical imaging analysis\nPredictive analytics for patient outcomes\nHealthcare workflow automation\nTelehealth solutions\n\nIs there a specific area you'd like more information about?",
            "ai": "Our healthcare AI solutions include diagnostic assistance, medical image analysis, patient risk prediction, and treatment recommendation systems.",
            "automation": "For healthcare automation, we offer appointment scheduling, patient records management, billing automation, and clinical workflow optimization.",
            "data": "Our healthcare data analytics includes patient outcome tracking, population health insights, operational efficiency metrics, and clinical trial data analysis."
        },
        "agriculture": {
            "general": "In agriculture, we assist with farm monitoring systems, crop data analytics, and IoT dashboard integration.",
            "details": "Our agricultural solutions include:\n\nSmart farming IoT integration\nCrop yield prediction models\nPest and disease detection systems\nWeather data analysis and forecasting\nSupply chain optimization\nResource usage optimization (water, fertilizer)\n\nWhat specific agricultural challenge are you looking to solve?",
            "ai": "Our agricultural AI tools include crop disease detection, yield prediction, optimal planting time recommendations, and automated sorting systems.",
            "automation": "For agriculture automation, we offer irrigation control systems, equipment monitoring, harvest scheduling, and supply chain management.",
            "data": "Our agricultural data solutions include soil health monitoring, crop performance analytics, weather pattern analysis, and resource usage optimization."
        },
        "banking": {
            "general": "In banking, we help with compliance automation, credit risk dashboards, fraud detection, and smart reporting.",
            "details": "Our banking and finance solutions include:\n\nFraud detection systems\nRegulatory compliance automation\nCustomer behavior analytics\nCredit risk assessment tools\nTrading algorithms and analysis\nCustomer service automation\n\nWhich aspect of banking technology would you like to explore further?",
            "ai": "Our banking AI solutions include fraud detection, credit scoring models, customer churn prediction, and algorithmic trading systems.",
            "automation": "For banking automation, we offer compliance reporting, loan processing, document verification, and customer onboarding workflows.",
            "data": "Our banking data analytics includes transaction pattern analysis, risk modeling, customer segmentation, and performance benchmarking."
        }
    }
    
    # Services and topics knowledge base
    topics = {
        "services": "We offer four main service categories:\n\nAutomation - streamlining workflows and business processes\nData Analytics - transforming data into actionable insights\nAI Tools - intelligent solutions for complex problems\nCustom Development - bespoke software for your unique needs\n\nWhich would you like to explore further?",
        
        "automation": "Our automation services help streamline repetitive tasks and workflows using Python and other technologies. We can automate:\n\nData entry and processing\nReport generation\nEmail management and responses\nDocument processing\nBusiness workflow integration\n\nDo you have a specific process you're looking to automate?",
        
        "data": "Our data analytics services transform raw information into valuable insights. We offer:\n\nInteractive dashboards\nBusiness intelligence solutions\nData pipeline development\nPredictive analytics\nCustom reporting systems\n\nWhat kind of data challenges are you facing?",
        
        "ai": "Our AI solutions bring intelligence to your business processes. We build:\n\nCustom chatbots and virtual assistants\nRecommendation systems\nPredictive models\nNatural language processing tools\nComputer vision applications\n\nHow do you envision AI helping your business?",
        
        "portfolio": "Our portfolio showcases our diverse range of successful projects across healthcare, agriculture, banking, and more. You can view detailed case studies on our website under the Portfolio section. Would you like me to highlight a specific industry example?",
        
        "pricing": "Our pricing is customized based on project scope, complexity, and timeline. We offer flexible models including:\n\nFixed project pricing\nHourly rates\nRetainer packages\nMaintenance plans\n\nTo receive a personalized quote, please share details about your project needs via our enquiry form.",
        
        "contact": "You can reach our team through multiple channels:\n\nEmail: kennedysmithaz@gmail.com\nPhone: +254-706776303\nEnquiry form on our website\nSchedule a consultation through our Calendly link\n\nWhat's your preferred method of communication?",
        
        "custom": "We specialize in creating custom solutions tailored to your specific business needs. Our development process includes:\n\nDetailed requirements gathering\nCollaborative design\nAgile development\nThorough testing\nDeployment and training\n\nCould you share what specific challenge you're looking to solve?"
    }
    
    # Helper responses
    help_responses = {
        "general": "I'd be happy to help! I can provide information about our services in automation, data analytics, AI solutions, or discuss how we might address challenges in your industry. What would you like to know more about?",
        
        "enquiry": "To better assist you, I recommend filling out our enquiry form. This helps us understand your needs in detail and allows our team to prepare a tailored response. You can find the form on our Contact page. Would you like the direct link?",
        
        "not_helping": "I apologize for not being more helpful. I'd like to ensure you get the assistance you need. Would you prefer to:\n\nTry explaining your question differently\nSpeak directly with a team member\nSubmit an enquiry through our form\n\nPlease let me know how you'd like to proceed."
    }
    
    # Check if we're awaiting more details about a specific topic
    if context["awaiting_more_details"]:
        industry = context["last_topic"]
        if industry in industries:
            context["awaiting_more_details"] = False
            return industries[industry]["details"]
        else:
            context["awaiting_more_details"] = False
    
    # Check for negative feedback
    negative_patterns = [
        "not helping", "can't help", "wrong answer", "incorrect", 
        "that's wrong", "that is wrong", "useless", "bad answer",
        "not what i asked", "didn't answer", "didn't understand"
    ]
    
    for pattern in negative_patterns:
        if pattern in message:
            return help_responses["not_helping"]
    
    # Handle basic intents first
    if fuzzy_match(message, greetings):
        return "Hello! I'm your digital assistant. How can I help you today with our automation, data analytics, or AI solutions?"
    
    if fuzzy_match(message, thanks):
        return "You're very welcome! I'm glad I could assist. Is there anything else you'd like to know about our services or solutions?"
    
    if fuzzy_match(message, farewells):
        return "Thank you for chatting with me today. If you have any other questions in the future, I'll be here to help. Have a wonderful day!"
    
    # Check for contact or communication requests
    contact_keywords = ["contact", "reach you", "email", "phone", "talk to someone", "contact details", "get in touch"]
    if any(keyword in message for keyword in contact_keywords):
        return topics["contact"]
    
    # Look for more details requests
    more_details_patterns = ["more details", "tell me more", "additional information", "learn more", "elaborate", "explain more"]
    if any(pattern in message for pattern in more_details_patterns):
        # Check if we have a context to provide more details about
        if context["last_topic"] in industries:
            return industries[context["last_topic"]]["details"]
        elif context["last_topic"] in topics:
            return topics[context["last_topic"]]
        else:
            return "I'd be happy to provide more details. Could you please specify which aspect of our services you're interested in learning more about?"
    
    # Check for industry specific requests
    for industry in industries:
        if industry in message:
            context["last_topic"] = industry
            
            # Check if asking about a specific aspect within the industry
            if "ai" in message or "artificial intelligence" in message:
                return industries[industry]["ai"]
            elif "automation" in message or "automate" in message:
                return industries[industry]["automation"]
            elif "data" in message or "analytics" in message:
                return industries[industry]["data"]
            else:
                # Set flag for follow-up about details
                if "details" in message or "more" in message:
                    return industries[industry]["details"]
                else:
                    context["awaiting_more_details"] = True
                    return industries[industry]["general"]
    
    # Check for service type requests
    for topic in topics:
        if topic in message or fuzzy_match(message, [topic]):
            context["last_topic"] = topic
            return topics[topic]
    
    # Check for differences/comparisons
    comparison_patterns = ["difference between", "compare", "versus", "vs"]
    if any(pattern in message for pattern in comparison_patterns):
        if ("automat" in message and "ai" in message) or ("automation" in message and "ai" in message):
            return "Great question about the difference between automation and AI tools:\n\nAutomation focuses on streamlining repetitive tasks and workflows using predefined rules and scripts. It's excellent for consistent, rule-based processes.\n\nAI tools use machine learning and intelligence to handle complex, variable situations and can adapt to new data. They're ideal for tasks requiring judgment, prediction, or understanding unstructured data.\n\nMany of our solutions combine both approaches. Would you like to explore how this might apply to your industry?"
    
    # Handle help requests
    help_patterns = ["help", "assist", "support", "what can you do", "how can you help"]
    if any(pattern in message for pattern in help_patterns):
        return help_responses["general"]
    
    # Final fallback with better experience
    return "I want to make sure I understand your needs correctly. Could you please provide a bit more detail about what you're looking for? I'm here to help with information about our automation services, data analytics, AI solutions, or specific industry applications."

@api_view(['GET'])
def get_chat_history(request, session_id):
    messages = ChatMessage.objects.filter(session_id=session_id).order_by('timestamp')
    if not messages.exists():
        return Response({"error": "No chat history found for this session."}, status=status.HTTP_404_NOT_FOUND)

    serializer = ChatMessageSerializer(messages, many=True)
    return Response({"chat_history": serializer.data}, status=status.HTTP_200_OK)

class ChatMessageListCreateView(generics.ListCreateAPIView):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer