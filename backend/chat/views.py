from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ChatMessage
from .serializers import ChatMessageSerializer
from difflib import get_close_matches
import uuid
import re
import random
from datetime import datetime

# Enhanced session store with comprehensive context tracking
session_context = {}

class ConversationalBot:
    def __init__(self):
        self.personality_responses = {
            "friendly_greetings": [
                "Hello there! Great to meet you! I'm here to help you explore how our technology solutions can transform your business.",
                "Hi! Welcome! I'm excited to chat with you about how we can help solve your business challenges.",
                "Hey! Thanks for stopping by. I'd love to learn about your business and see how our automation, AI, and data solutions might help.",
                "Hello! I'm your digital assistant, and I'm genuinely excited to help you discover the perfect solution for your needs."
            ],
            "understanding_responses": [
                "That's a great question! Let me break that down for you...",
                "I love that you're thinking about this! Here's what I can tell you...",
                "Absolutely! That's something we help businesses with all the time. Here's how...",
                "Perfect question! This is actually one of our specialties..."
            ],
            "clarification_requests": [
                "That sounds interesting! Could you tell me a bit more about your specific situation?",
                "I want to make sure I give you the most helpful information. What industry are you in?",
                "Great! To give you the best recommendations, could you share more about your current challenges?",
                "I'd love to help you with that! What's your main goal with this project?"
            ]
        }
        
        self.industry_expertise = {
            "healthcare": {
                "intro": "Healthcare is one of our strongest areas! We've helped hospitals, clinics, and healthcare organizations streamline their operations and improve patient care.",
                "services": {
                    "patient_management": "We build comprehensive patient management systems that handle everything from appointment scheduling to medical records. These systems can integrate with existing EMR systems and provide real-time dashboards for healthcare providers.",
                    "ai_diagnostics": "Our AI diagnostic tools help medical professionals by analyzing medical images, predicting patient risks, and suggesting treatment options based on historical data and current best practices.",
                    "telemedicine": "We develop telemedicine platforms that are secure, HIPAA-compliant, and user-friendly for both patients and healthcare providers.",
                    "workflow_automation": "We automate repetitive healthcare workflows like insurance verification, billing processes, and appointment reminders, freeing up staff to focus on patient care.",
                    "data_analytics": "Our healthcare analytics provide insights into patient outcomes, operational efficiency, cost optimization, and population health trends."
                },
                "examples": "For instance, we recently helped a medical clinic reduce patient wait times by 40% through automated scheduling and workflow optimization. We also built an AI system for a diagnostic center that improved accuracy in radiology reports by 25%.",
                "compliance": "All our healthcare solutions are built with HIPAA compliance, data security, and patient privacy as top priorities."
            },
            "agriculture": {
                "intro": "Agriculture and agtech are fascinating fields where technology can make a huge impact! We help farmers and agricultural businesses optimize their operations through smart technology.",
                "services": {
                    "smart_farming": "We develop IoT-based smart farming solutions that monitor soil conditions, weather patterns, and crop health in real-time. Farmers get automated alerts and recommendations through mobile apps.",
                    "crop_analytics": "Our AI analyzes satellite imagery, weather data, and soil conditions to predict optimal planting times, harvest schedules, and yield estimates.",
                    "precision_agriculture": "We build systems that optimize resource usage - water, fertilizers, and pesticides - based on real-time field conditions and historical data.",
                    "supply_chain": "We create supply chain management systems that track produce from farm to market, ensuring quality control and reducing waste.",
                    "livestock_monitoring": "Our IoT solutions monitor livestock health, feeding patterns, and environmental conditions to optimize animal welfare and productivity."
                },
                "examples": "We helped a 500-acre farm increase crop yield by 30% while reducing water usage by 25% through our precision irrigation system. Another client saw a 50% reduction in crop loss through our early disease detection system.",
                "sustainability": "All our agricultural solutions focus on sustainable farming practices that benefit both the environment and profitability."
            },
            "banking": {
                "intro": "Banking and fintech are areas where security, compliance, and user experience are absolutely critical. We understand these challenges deeply.",
                "services": {
                    "fraud_detection": "Our AI-powered fraud detection systems analyze transaction patterns in real-time to identify suspicious activities, reducing false positives while catching actual fraud.",
                    "compliance_automation": "We automate regulatory reporting, KYC processes, and compliance monitoring to ensure banks meet all regulatory requirements efficiently.",
                    "customer_analytics": "Our analytics platforms help banks understand customer behavior, predict churn, and personalize services to improve customer satisfaction and retention.",
                    "digital_banking": "We develop secure mobile banking apps and online platforms with features like biometric authentication, real-time notifications, and seamless user experiences.",
                    "risk_management": "Our risk assessment tools use machine learning to evaluate credit risks, market risks, and operational risks with greater accuracy than traditional methods."
                },
                "examples": "We built a fraud detection system for a regional bank that reduced fraudulent transactions by 60% while improving customer experience. Our compliance automation solution helped another client reduce regulatory reporting time from weeks to hours.",
                "security": "Every banking solution we build follows the highest security standards with encryption, secure APIs, and regular security audits."
            },
            "retail": {
                "intro": "Retail is all about understanding customers and optimizing operations. We help retailers leverage technology to improve both!",
                "services": {
                    "inventory_management": "Smart inventory systems that predict demand, automate reordering, and optimize stock levels across multiple locations.",
                    "customer_analytics": "Deep customer behavior analysis to personalize marketing, optimize pricing, and improve customer experience.",
                    "recommendation_engines": "AI-powered recommendation systems that increase sales by suggesting relevant products to customers.",
                    "pos_integration": "Modern point-of-sale systems that integrate with inventory, customer management, and analytics platforms.",
                    "supply_chain": "End-to-end supply chain optimization from suppliers to customers, including demand forecasting and logistics optimization."
                }
            },
            "education": {
                "intro": "Education technology is incredibly rewarding! We help educational institutions improve learning outcomes and operational efficiency.",
                "services": {
                    "learning_management": "Custom learning management systems with features like adaptive learning, progress tracking, and interactive content delivery.",
                    "student_analytics": "Analytics platforms that help educators identify at-risk students and personalize learning approaches.",
                    "automation": "Administrative automation for enrollment, scheduling, grading, and communication with students and parents.",
                    "virtual_classrooms": "Interactive online learning platforms with video conferencing, collaboration tools, and assessment features."
                }
            }
        }
        
        self.service_details = {
            "automation": {
                "description": "Automation is about making your business run smoother by handling repetitive tasks automatically. Think of it as having a tireless digital assistant that never makes mistakes!",
                "benefits": [
                    "Save hours of manual work every day",
                    "Reduce human errors and improve accuracy", 
                    "Free up your team to focus on high-value activities",
                    "Ensure consistent processes across your organization",
                    "Scale operations without proportionally increasing staff"
                ],
                "examples": {
                    "document_processing": "We can automate invoice processing, contract generation, report creation, and data entry from various sources.",
                    "workflow_automation": "Automated approval workflows, task assignments, notifications, and follow-ups based on business rules.",
                    "data_synchronization": "Automatic data syncing between different systems, databases, and applications.",
                    "communication": "Automated email responses, customer notifications, and internal team updates.",
                    "scheduling": "Smart scheduling systems for appointments, meetings, and resource allocation."
                },
                "technologies": "We use Python, RPA tools, API integrations, and cloud platforms to build robust automation solutions.",
                "roi": "Most of our automation projects pay for themselves within 6-12 months through time savings and error reduction."
            },
            "ai": {
                "description": "AI isn't just buzzword technology - it's practical intelligence that can solve real business problems by learning from data and making smart decisions.",
                "capabilities": [
                    "Predict future trends and outcomes",
                    "Understand and process natural language",
                    "Recognize patterns in images and videos",
                    "Make recommendations based on user behavior",
                    "Automate complex decision-making processes"
                ],
                "applications": {
                    "chatbots": "Intelligent customer service bots that understand context and provide helpful, human-like responses.",
                    "predictive_analytics": "Forecast sales, predict equipment failures, or identify market opportunities before they happen.",
                    "computer_vision": "Analyze images for quality control, medical diagnosis, or security monitoring.",
                    "recommendation_systems": "Suggest products, content, or actions based on user preferences and behavior patterns.",
                    "natural_language": "Analyze customer feedback, automate document review, or extract insights from text data."
                },
                "approach": "We don't just implement AI for the sake of it - we identify specific business problems where AI can provide measurable value.",
                "ethics": "We build responsible AI that's transparent, fair, and respects privacy while delivering business results."
            },
            "data_analytics": {
                "description": "Data analytics transforms the information you already have into actionable insights that drive better business decisions.",
                "value_proposition": "Most businesses are sitting on goldmines of data but don't know how to extract value from it. We change that!",
                "offerings": {
                    "dashboards": "Beautiful, interactive dashboards that give you real-time visibility into your business performance with drill-down capabilities.",
                    "reporting": "Automated report generation that delivers key insights to stakeholders on schedule, customized for different roles.",
                    "predictive_analytics": "Use historical data to predict future trends, customer behavior, and potential risks or opportunities.",
                    "data_integration": "Combine data from multiple sources into a unified view of your business operations.",
                    "visualization": "Transform complex data into clear, compelling visual stories that anyone can understand."
                },
                "process": "We start by understanding your key business questions, then build analytics solutions that directly answer those questions with clear, actionable insights.",
                "tools": "We use modern tools like Python, R, Tableau, Power BI, and cloud analytics platforms to deliver powerful solutions."
            },
            "custom_development": {
                "description": "Sometimes off-the-shelf solutions just don't fit your unique business needs. That's where custom development shines!",
                "when_needed": [
                    "Your business processes are unique and competitive advantages",
                    "Existing software doesn't integrate well with your systems",
                    "You need specific features that aren't available in standard products",
                    "Compliance or security requirements demand custom solutions",
                    "You want to create new revenue streams through technology"
                ],
                "approach": {
                    "discovery": "We start with deep discovery sessions to understand your business, challenges, and goals.",
                    "design": "Collaborative design process where we prototype and refine solutions with your input.",
                    "development": "Agile development with regular check-ins and opportunities for feedback.",
                    "testing": "Comprehensive testing to ensure reliability, security, and performance.",
                    "deployment": "Smooth deployment with training and ongoing support."
                },
                "technologies": "We work with modern web technologies, mobile platforms, cloud infrastructure, and databases to build scalable, secure solutions."
            }
        }

    def get_random_response(self, category):
        """Get a random response from a category to add personality"""
        return random.choice(self.personality_responses.get(category, ["I understand!"]))

    def extract_intent(self, message, context):
        """Extract user intent from message with context awareness"""
        message_lower = message.lower()
        
        # Define intent patterns
        intents = {
            "greeting": ["hello", "hi", "hey", "good morning", "good afternoon", "good evening", "greetings"],
            "thanks": ["thank", "thanks", "appreciate", "grateful"],
            "goodbye": ["bye", "goodbye", "see you", "take care", "farewell", "later"],
            "help": ["help", "assist", "support", "guide", "what can you do"],
            "services": ["services", "what do you offer", "offerings", "solutions"],
            "pricing": ["price", "cost", "pricing", "how much", "budget", "quote"],
            "contact": ["contact", "reach", "email", "phone", "talk to someone", "get in touch",
                        "human support", "talk to a human", "real person", "speak to someone", "talk to a person"],
            "portfolio": ["portfolio", "examples", "case studies", "previous work", "projects"],
            "industry_specific": list(self.industry_expertise.keys()),
            "service_specific": list(self.service_details.keys()),
            "website": ["website", "web development", "web design", "online presence"],
            "more_info": ["more", "details", "tell me more", "elaborate", "explain", "additional information"],
            "comparison": ["difference", "compare", "versus", "vs", "better", "which one"],
            "implementation": ["how do you", "process", "approach", "methodology", "timeline"],
            "negative_feedback": ["not helpful", "wrong", "incorrect", "bad", "useless", "not what i asked"]
        }
        
        detected_intents = []
        
        for intent, keywords in intents.items():
            if intent == "industry_specific":
                for industry in keywords:
                    if industry in message_lower:
                        detected_intents.append(("industry", industry))
            elif intent == "service_specific":
                for service in keywords:
                    if service in message_lower or any(keyword in message_lower for keyword in [service, service.replace("_", " ")]):
                        detected_intents.append(("service", service))
            else:
                if any(keyword in message_lower for keyword in keywords):
                    detected_intents.append((intent, None))
        
        return detected_intents

    def handle_greeting(self, context):
        """Handle greeting with personality"""
        greeting = self.get_random_response("friendly_greetings")
        context["conversation_stage"] = "engaged"
        return greeting

    def handle_industry_inquiry(self, industry, message, context):
        """Handle industry-specific inquiries with detailed responses"""
        industry_info = self.industry_expertise.get(industry, {})
        message_lower = message.lower()
        
        # Check if asking about specific aspects
        if any(term in message_lower for term in ["ai", "artificial intelligence", "machine learning"]):
            response = f"{industry_info.get('intro', '')}\n\nRegarding AI in {industry}:\n"
            ai_services = [service for key, service in industry_info.get('services', {}).items() if 'ai' in key.lower() or 'analytics' in service.lower()]
            if ai_services:
                response += "\n".join(f"• {service}" for service in ai_services[:2])
            else:
                response += f"We implement AI solutions tailored to {industry} challenges, including predictive analytics, automation, and intelligent decision-making systems."
        
        elif any(term in message_lower for term in ["automat", "workflow", "process"]):
            response = f"{industry_info.get('intro', '')}\n\nFor {industry} automation:\n"
            auto_services = [service for key, service in industry_info.get('services', {}).items() if 'automat' in service.lower() or 'workflow' in service.lower()]
            if auto_services:
                response += "\n".join(f"• {service}" for service in auto_services[:2])
            else:
                response += f"We streamline {industry} operations through intelligent automation of repetitive tasks and workflows."
        
        elif any(term in message_lower for term in ["data", "analytics", "reporting"]):
            response = f"{industry_info.get('intro', '')}\n\nOur {industry} data solutions include:\n"
            data_services = [service for key, service in industry_info.get('services', {}).items() if 'data' in service.lower() or 'analytic' in service.lower()]
            if data_services:
                response += "\n".join(f"• {service}" for service in data_services[:2])
            else:
                response += f"We transform {industry} data into actionable insights through advanced analytics and visualization."
        
        elif "website" in message_lower:
            response = f"Absolutely! We create specialized websites for {industry} businesses.\n\n"
            response += f"For {industry}, we typically build:\n"
            if industry == "healthcare":
                response += "• Patient portals with appointment scheduling\n• HIPAA-compliant telemedicine platforms\n• Medical practice websites with secure communication\n• Health information management systems"
            elif industry == "agriculture":
                response += "• Farm management dashboards\n• Agricultural marketplace platforms\n• Crop monitoring web applications\n• Supply chain tracking systems"
            elif industry == "banking":
                response += "• Secure online banking platforms\n• Financial services websites\n• Investment portfolio dashboards\n• Compliance reporting systems"
            else:
                response += f"• Professional {industry} websites with modern design\n• Industry-specific functionality and features\n• Mobile-responsive and user-friendly interfaces\n• Integration with your existing systems"
        
        else:
            # General industry response
            response = industry_info.get('intro', f"We have extensive experience working with {industry} businesses!")
            
            if 'services' in industry_info:
                response += f"\n\nOur key {industry} solutions include:\n"
                services_list = list(industry_info['services'].values())[:3]  # Show first 3 services
                response += "\n".join(f"• {service.split('.')[0]}." for service in services_list)
            
            if 'examples' in industry_info:
                response += f"\n\n{industry_info['examples']}"
        
        # Add follow-up question
        follow_ups = [
            f"What specific challenges are you facing in your {industry} business?",
            f"Which aspect of {industry} technology interests you most?",
            f"Are you looking to solve a particular problem in your {industry} operations?",
            f"What's your main goal for implementing technology in your {industry} business?"
        ]
        response += f"\n\n{random.choice(follow_ups)}"
        
        context["last_topic"] = industry
        context["conversation_stage"] = "exploring"
        
        return response

    def handle_service_inquiry(self, service, message, context):
        """Handle service-specific inquiries with comprehensive information"""
        service_info = self.service_details.get(service, {})
        message_lower = message.lower()
        
        response = f"{self.get_random_response('understanding_responses')}\n\n"
        response += service_info.get('description', f"Let me tell you about our {service} services!")
        
        # Add specific details based on the service
        if service == "automation":
            response += f"\n\nHere's what automation can do for you:\n"
            response += "\n".join(f"• {benefit}" for benefit in service_info.get('benefits', [])[:4])
            
            response += f"\n\nCommon automation examples:\n"
            examples = service_info.get('examples', {})
            response += "\n".join(f"• {desc}" for desc in list(examples.values())[:3])
            
            response += f"\n\n{service_info.get('roi', '')}"
        
        elif service == "ai":
            response += f"\n\nOur AI solutions can:\n"
            response += "\n".join(f"• {capability}" for capability in service_info.get('capabilities', [])[:4])
            
            response += f"\n\nPopular AI applications we build:\n"
            apps = service_info.get('applications', {})
            response += "\n".join(f"• {desc}" for desc in list(apps.values())[:3])
        
        elif service == "data_analytics":
            response += f"\n\n{service_info.get('value_proposition', '')}"
            
            response += f"\n\nOur analytics offerings include:\n"
            offerings = service_info.get('offerings', {})
            response += "\n".join(f"• {desc}" for desc in list(offerings.values())[:3])
        
        elif service == "custom_development":
            response += f"\n\nCustom development is perfect when:\n"
            response += "\n".join(f"• {reason}" for reason in service_info.get('when_needed', [])[:4])
        
        # Add contextual follow-up
        if any(word in message_lower for word in ["how", "process", "work", "approach"]):
            if 'approach' in service_info:
                response += f"\n\nOur {service} process:\n"
                approach = service_info['approach']
                if isinstance(approach, dict):
                    response += "\n".join(f"• {step.title()}: {desc}" for step, desc in list(approach.items())[:3])
                else:
                    response += approach
        
        # Industry-specific follow-up if context available
        if context.get("last_topic") in self.industry_expertise:
            industry = context["last_topic"]
            response += f"\n\nFor {industry} businesses specifically, {service} can be particularly powerful. Would you like to explore how {service} applies to your {industry} operations?"
        else:
            response += f"\n\nWhat type of business challenges are you hoping {service} might solve for you?"
        
        context["last_topic"] = service
        context["conversation_stage"] = "detailed_discussion"
        
        return response

    def handle_website_inquiry(self, message, context):
        """Handle website development inquiries"""
        message_lower = message.lower()
        
        response = "Absolutely! We create powerful, modern websites that go beyond just looking good - they're built to drive results for your business.\n\n"
        
        # Check if they've mentioned an industry
        user_industry = None
        for industry in self.industry_expertise.keys():
            if industry in message_lower:
                user_industry = industry
                break
        
        if user_industry:
            response += f"For {user_industry} businesses, we typically create:\n"
            if user_industry == "healthcare":
                response += "• Patient portals with secure appointment scheduling\n• HIPAA-compliant websites with telemedicine integration\n• Medical practice sites with online forms and communication tools\n• Health information systems with real-time dashboards"
            elif user_industry == "agriculture":
                response += "• Farm management platforms with IoT integration\n• Agricultural marketplace and e-commerce sites\n• Crop monitoring dashboards with real-time data\n• Supply chain tracking and management systems"
            elif user_industry == "banking":
                response += "• Secure online banking platforms with advanced security\n• Financial services websites with client portals\n• Investment tracking and reporting dashboards\n• Regulatory compliance and reporting systems"
            else:
                response += f"• Professional {user_industry} websites with industry-specific features\n• Custom functionality tailored to your business needs\n• Integration with your existing systems and workflows\n• Mobile-responsive design optimized for your customers"
        else:
            response += "Our websites include:\n"
            response += "• Modern, responsive designs that work perfectly on all devices\n"
            response += "• Custom functionality tailored to your business needs\n"
            response += "• Integration with your existing systems and databases\n"
            response += "• SEO optimization and performance optimization\n"
            response += "• Content management systems that are easy to update\n"
            response += "• E-commerce capabilities if needed\n"
            response += "• Analytics and tracking to measure success"
        
        response += "\n\nWe don't just build websites - we create digital experiences that help you achieve your business goals. "
        response += "Every website we build is custom-designed around your specific needs, brand, and target audience.\n\n"
        
        # Ask clarifying questions
        if not user_industry:
            response += "What industry are you in? This helps me suggest the most relevant features for your website."
        else:
            response += f"What's the main goal for your {user_industry} website? Are you looking to attract new clients, streamline operations, or something else?"
        
        context["last_topic"] = "website"
        context["conversation_stage"] = "requirements_gathering"
        
        return response

    def handle_pricing_inquiry(self, context):
        """Handle pricing questions with value-focused approach"""
        response = "Great question about pricing! I appreciate that budget is an important consideration.\n\n"
        response += "Our pricing is always customized because every business has unique needs, but I can give you some helpful context:\n\n"
        
        response += "**Our Pricing Approach:**\n"
        response += "• We provide fixed-price quotes so you know exactly what to expect\n"
        response += "• Pricing depends on project scope, complexity, and timeline\n"
        response += "• We offer flexible payment terms and can work with most budgets\n"
        response += "• Most of our projects pay for themselves through efficiency gains\n\n"
        
        response += "**Typical Investment Ranges:**\n"
        response += "• Simple automation projects: Often start around $2,000-5,000\n"
        response += "• Custom websites with advanced features: $5,000-15,000\n"
        response += "• AI and analytics solutions: $10,000-25,000+\n"
        response += "• Comprehensive business systems: $15,000-50,000+\n\n"
        
        response += "The best way to get an accurate quote is to discuss your specific needs. "
        response += "We can often find creative ways to deliver value within your budget.\n\n"
        response += "What type of project are you considering? I'd be happy to give you a more specific range based on your needs."
        
        context["conversation_stage"] = "pricing_discussion"
        return response

    def handle_contact_inquiry(self, context):
        """Handle contact and communication requests"""
        response = "I'd be happy to connect you with our team! Here are the best ways to reach us:\n\n"
        response += "**Direct Contact:**\n"
        response += "• Email: kennedysmithaz@gmail.com\n"
        response += "• Phone: +254-706776303\n"
        response += "• We typically respond within a few hours during business days\n\n"
        
        response += "**For Detailed Discussions:**\n"
        response += "• Fill out our enquiry form on the website for comprehensive project discussions\n"
        response += "• Schedule a free consultation call to explore your needs in detail\n"
        response += "• We can arrange video calls for more complex projects\n\n"
        
        response += "Based on our conversation, it sounds like you're interested in "
        if context.get("last_topic"):
            response += f"{context['last_topic']} solutions. "
        response += "I'd recommend mentioning this when you reach out so our team can prepare relevant examples and ideas for you.\n\n"
        
        response += "Would you prefer to start with an email, phone call, or would you like me to guide you to our enquiry form?"
        
        context["conversation_stage"] = "ready_to_connect"
        return response

    def handle_comparison_request(self, message, context):
        """Handle comparison questions between services or approaches"""
        message_lower = message.lower()
        
        if ("automation" in message_lower and "ai" in message_lower):
            response = "Excellent question! This is something many businesses wonder about. Let me break down the key differences:\n\n"
            response += "**Automation** is like having a very reliable assistant that follows specific rules:\n"
            response += "• Perfect for repetitive, rule-based tasks\n"
            response += "• Handles structured processes consistently\n"
            response += "• Great for data entry, report generation, workflow management\n"
            response += "• Usually faster to implement and more predictable\n\n"
            
            response += "**AI** is like having a smart colleague that can learn and adapt:\n"
            response += "• Handles complex, variable situations\n"
            response += "• Can make decisions based on patterns in data\n"
            response += "• Perfect for predictions, recommendations, understanding text/images\n"
            response += "• Gets smarter over time with more data\n\n"
            
            response += "**The Sweet Spot:** Many of our best solutions combine both! For example, we might use AI to analyze customer data and predict needs, then use automation to act on those insights.\n\n"
            
            if context.get("last_topic") in self.industry_expertise:
                industry = context["last_topic"]
                response += f"In {industry}, we often see automation handling routine tasks while AI tackles the complex decision-making. "
            
            response += "What kind of business challenge are you looking to solve? I can suggest whether automation, AI, or a combination would work best."
        
        else:
            response = "I'd be happy to help you compare different approaches! "
            response += "Could you be more specific about what you'd like me to compare? "
            response += "For example, are you wondering about different types of solutions, pricing models, or implementation approaches?"
        
        return response

    def handle_implementation_question(self, message, context):
        """Handle questions about process, timeline, and methodology"""
        response = "Great question! Our implementation process is designed to ensure success while minimizing disruption to your business.\n\n"
        
        response += "**Our Proven Process:**\n\n"
        response += "**1. Discovery & Planning (1-2 weeks)**\n"
        response += "• Deep dive into your business needs and current processes\n"
        response += "• Technical assessment of existing systems\n"
        response += "• Define clear goals and success metrics\n"
        response += "• Create detailed project plan and timeline\n\n"
        
        response += "**2. Design & Prototyping (1-3 weeks)**\n"
        response += "• Create mockups and prototypes for your review\n"
        response += "• Collaborative design sessions to refine the solution\n"
        response += "• Technical architecture planning\n"
        response += "• Get your approval before development begins\n\n"
        
        response += "**3. Development & Testing (2-8 weeks)**\n"
        response += "• Agile development with regular progress updates\n"
        response += "• Weekly check-ins and demonstrations\n"
        response += "• Comprehensive testing for reliability and security\n"
        response += "• User acceptance testing with your team\n\n"
        
        response += "**4. Deployment & Training (1-2 weeks)**\n"
        response += "• Smooth deployment with minimal business disruption\n"
        response += "• Comprehensive training for your team\n"
        response += "• Documentation and support materials\n"
        response += "• Go-live support to ensure everything runs smoothly\n\n"
        
        response += "**5. Ongoing Support**\n"
        response += "• Post-launch support and monitoring\n"
        response += "• Regular check-ins to ensure optimal performance\n"
        response += "• Updates and enhancements as needed\n\n"
        
        if context.get("last_topic"):
            topic = context["last_topic"]
            response += f"For {topic} projects specifically, "
            if topic == "automation":
                response += "we typically see results within the first month of deployment."
            elif topic == "ai":
                response += "the AI models improve over time as they learn from your data."
            elif topic in self.industry_expertise:
                response += f"we follow {topic} industry best practices and compliance requirements."
            else:
                response += "we tailor our approach to your specific requirements."
        
        response += "\n\nTypical project timelines range from 4-12 weeks depending on complexity. What kind of timeline are you working with?"
        
        context["conversation_stage"] = "implementation_discussion"
        return response

    def handle_negative_feedback(self, message, context):
        """Handle negative feedback constructively"""
        responses = [
            "I apologize that my previous response wasn't helpful! Let me try a different approach.",
            "You're absolutely right - let me give you a better answer to your question.",
            "I hear you, and I want to make sure I give you exactly what you're looking for.",
            "Thanks for the feedback - let me be more specific and helpful."
        ]
        
        response = random.choice(responses)
        response += "\n\nTo better assist you, could you help me understand:\n"
        response += "• What specific information are you looking for?\n"
        response += "• What would be most helpful for your situation?\n"
        response += "• Are there particular aspects of our services you want to focus on?\n\n"
        response += "I'm here to provide exactly the information you need, so please don't hesitate to guide me in the right direction!"
        
        context["conversation_stage"] = "recovery"
        return response

    def generate_contextual_response(self, message, context):
        """Generate contextually aware responses"""
        intents = self.extract_intent(message, context)
        
        if not intents:
            # Handle unstructured queries with intelligence
            return self.handle_open_ended_query(message, context)
        
        # Process multiple intents intelligently
        primary_intent = intents[0]
        intent_type, intent_value = primary_intent
        
        # Handle different intent types
        if intent_type == "greeting":
            return self.handle_greeting(context)
        elif intent_type == "thanks":
            return "You're very welcome! I'm really glad I could help. Is there anything else you'd like to explore about our services?"
        elif intent_type == "goodbye":
            return "Thank you for the great conversation! Feel free to reach out anytime if you have more questions. Have a wonderful time!"
        elif intent_type == "industry":
            return self.handle_industry_inquiry(intent_value, message, context)
        elif intent_type == "service":
            return self.handle_service_inquiry(intent_value, message, context)
        elif intent_type == "website":
            return self.handle_website_inquiry(message, context)
        elif intent_type == "pricing":
            return self.handle_pricing_inquiry(context)
        elif intent_type == "contact":
            return self.handle_contact_inquiry(context)
        elif intent_type == "comparison":
            return self.handle_comparison_request(message, context)
        elif intent_type == "implementation":
            return self.handle_implementation_question(message, context)
        elif intent_type == "negative_feedback":
            return self.handle_negative_feedback(message, context)
        elif intent_type == "more_info":
            return self.handle_more_info_request(message, context)
        elif intent_type == "help":
            return self.handle_help_request(context)
        elif intent_type == "services":
            return self.handle_services_overview(context)
        elif intent_type == "portfolio":
            return self.handle_portfolio_request(context)
        else:
            return self.handle_open_ended_query(message, context)

    def handle_more_info_request(self, message, context):
        """Handle requests for more information"""
        last_topic = context.get("last_topic")
        
        if last_topic in self.industry_expertise:
            industry_info = self.industry_expertise[last_topic]
            response = f"Absolutely! Let me dive deeper into our {last_topic} solutions.\n\n"
            
            # Provide comprehensive industry information
            if 'services' in industry_info:
                response += f"**Our Comprehensive {last_topic.title()} Services:**\n\n"
                for i, (key, service) in enumerate(industry_info['services'].items(), 1):
                    response += f"**{i}. {key.replace('_', ' ').title()}**\n{service}\n\n"
            
            if 'examples' in industry_info:
                response += f"**Success Stories:**\n{industry_info['examples']}\n\n"
            
            if 'compliance' in industry_info:
                response += f"**Compliance & Security:**\n{industry_info['compliance']}\n\n"
            
            response += f"What specific aspect of {last_topic} technology would you like to explore further?"
            
        elif last_topic in self.service_details:
            service_info = self.service_details[last_topic]
            response = f"Perfect! Let me give you the complete picture of our {last_topic} capabilities.\n\n"
            
            # Provide comprehensive service information
            if 'description' in service_info:
                response += f"{service_info['description']}\n\n"
            
            if 'benefits' in service_info:
                response += f"**Key Benefits:**\n"
                response += "\n".join(f"• {benefit}" for benefit in service_info['benefits']) + "\n\n"
            
            if 'examples' in service_info:
                response += f"**What We Can Automate:**\n"
                for category, desc in service_info['examples'].items():
                    response += f"• **{category.replace('_', ' ').title()}**: {desc}\n"
                response += "\n"
            
            if 'applications' in service_info:
                response += f"**Applications We Build:**\n"
                for app, desc in service_info['applications'].items():
                    response += f"• **{app.replace('_', ' ').title()}**: {desc}\n"
                response += "\n"
            
            if 'approach' in service_info:
                response += f"**Our Approach:**\n"
                approach = service_info['approach']
                if isinstance(approach, dict):
                    for step, desc in approach.items():
                        response += f"• **{step.title()}**: {desc}\n"
                else:
                    response += f"{approach}\n"
                response += "\n"
            
            response += f"Is there a particular aspect of {last_topic} you'd like to discuss for your specific situation?"
            
        else:
            response = "I'd love to provide more details! What specifically would you like to know more about? "
            response += "I can dive deeper into any of our services (automation, AI, data analytics, custom development) "
            response += "or discuss how we work with specific industries like healthcare, agriculture, or banking."
        
        context["conversation_stage"] = "deep_dive"
        return response

    def handle_help_request(self, context):
        """Handle general help requests"""
        response = "I'm here to help you discover how our technology solutions can transform your business! "
        response += "I can assist you with information about:\n\n"
        
        response += "**Our Services:**\n"
        response += "• **Automation** - Streamline repetitive tasks and workflows\n"
        response += "• **AI Solutions** - Intelligent tools for complex business challenges\n"
        response += "• **Data Analytics** - Transform data into actionable insights\n"
        response += "• **Custom Development** - Bespoke software solutions\n"
        response += "• **Website Development** - Modern, results-driven websites\n\n"
        
        response += "**Industry Expertise:**\n"
        response += "• Healthcare & Medical\n• Agriculture & Farming\n• Banking & Finance\n• Retail & E-commerce\n• Education\n\n"
        
        response += "**I Can Help With:**\n"
        response += "• Understanding which solutions fit your needs\n"
        response += "• Explaining our process and approach\n"
        response += "• Discussing pricing and timelines\n"
        response += "• Connecting you with our team\n"
        response += "• Sharing relevant examples and case studies\n\n"
        
        response += "What interests you most? Or tell me about your business challenge and I'll suggest the best solutions!"
        
        context["conversation_stage"] = "guidance"
        return response

    def handle_services_overview(self, context):
        """Handle requests for services overview"""
        response = "Excellent! I'm excited to share what we can do for your business. We offer comprehensive technology solutions designed to solve real business problems:\n\n"
        
        response += "**🤖 Automation Services**\n"
        response += "Make your business run smoother by automating repetitive tasks. Think document processing, data entry, workflow management, and report generation. Most clients see ROI within 6-12 months!\n\n"
        
        response += "**🧠 AI Solutions**\n"
        response += "Intelligent tools that learn and adapt to your business. We build chatbots, predictive analytics, recommendation systems, and decision-making tools that get smarter over time.\n\n"
        
        response += "**📊 Data Analytics**\n"
        response += "Transform your data into powerful insights with interactive dashboards, automated reporting, and predictive analytics. See patterns you never noticed and make data-driven decisions.\n\n"
        
        response += "**💻 Custom Development**\n"
        response += "When off-the-shelf solutions don't fit, we build exactly what you need. Web applications, mobile apps, databases, and integrations tailored to your unique requirements.\n\n"
        
        response += "**🌐 Website Development**\n"
        response += "Modern, responsive websites that drive results. From simple business sites to complex web applications with advanced functionality.\n\n"
        
        response += "**Industry Specializations:**\n"
        response += "We have deep expertise in Healthcare, Agriculture, Banking, Retail, and Education - but we work with businesses across all industries.\n\n"
        
        response += "What type of challenges is your business facing? I can recommend the perfect combination of services for your needs!"
        
        context["conversation_stage"] = "service_exploration"
        return response

    def handle_portfolio_request(self, context):
        """Handle portfolio and examples requests"""
        response = "I'd love to share some examples of our work! We've helped businesses across many industries achieve amazing results:\n\n"
        
        response += "**Healthcare Success Stories:**\n"
        response += "• Reduced patient wait times by 40% through automated scheduling for a medical clinic\n"
        response += "• Built HIPAA-compliant telemedicine platform serving 1000+ patients\n"
        response += "• Created AI diagnostic tool that improved radiology accuracy by 25%\n\n"
        
        response += "**Agriculture Innovations:**\n"
        response += "• Smart irrigation system increased crop yield by 30% while reducing water usage by 25%\n"
        response += "• Early disease detection system reduced crop loss by 50% for a 500-acre farm\n"
        response += "• Supply chain tracking system eliminated 90% of manual paperwork\n\n"
        
        response += "**Banking Solutions:**\n"
        response += "• Fraud detection system reduced fraudulent transactions by 60%\n"
        response += "• Compliance automation reduced regulatory reporting time from weeks to hours\n"
        response += "• Customer analytics platform improved retention by 35%\n\n"
        
        response += "**Business Automation:**\n"
        response += "• Invoice processing automation saved 20 hours/week for accounting firm\n"
        response += "• Customer service chatbot handles 80% of inquiries automatically\n"
        response += "• Data synchronization between 5 systems eliminated manual errors\n\n"
        
        response += "These are just a few highlights! Each project was custom-built to solve specific business challenges.\n\n"
        response += "What industry are you in? I can share more relevant examples and discuss how similar solutions might help your business!"
        
        context["conversation_stage"] = "examples_discussion"
        return response

    def handle_open_ended_query(self, message, context):
        """Handle unstructured or complex queries intelligently"""
        message_lower = message.lower()
        
        # Check for business problems or pain points
        pain_points = {
            "time": "It sounds like you're looking to save time and increase efficiency! Our automation solutions are perfect for this.",
            "manual": "Manual processes can be such a drain on productivity! We specialize in automating repetitive tasks.",
            "data": "Data challenges are incredibly common. Our analytics solutions help businesses make sense of their information.",
            "customers": "Customer-related challenges are where technology can make a huge impact! We build solutions that improve customer experience.",
            "cost": "Cost reduction is often a key benefit of our solutions. Most of our automation projects pay for themselves within a year.",
            "growth": "Growth challenges are exciting! We build scalable solutions that grow with your business.",
            "efficiency": "Efficiency improvements are at the heart of what we do. Technology can dramatically streamline operations.",
            "decision": "Better decision-making comes from better data insights. Our analytics solutions provide exactly that."
        }
        
        for pain_point, response_start in pain_points.items():
            if pain_point in message_lower:
                response = f"{response_start}\n\n"
                response += "Tell me more about your specific situation:\n"
                response += "• What industry is your business in?\n"
                response += "• What's the biggest challenge you're facing?\n"
                response += "• What would success look like for you?\n\n"
                response += "With more details, I can suggest the perfect solution for your needs!"
                return response
        
        # Check for technology interest
        tech_terms = ["technology", "software", "system", "platform", "solution", "tool"]
        if any(term in message_lower for term in tech_terms):
            response = "Technology solutions can be game-changers for businesses! "
            response += "We help companies leverage automation, AI, data analytics, and custom development to solve real business problems.\n\n"
            response += "What kind of technology challenge are you trying to solve? Or what business process would you like to improve?\n\n"
            response += "I can help you explore the best approach for your specific needs!"
            return response
        
        # Default intelligent response
        response = "That's an interesting question! I want to make sure I give you the most helpful information. "
        response += "Let me ask a couple of questions to better understand your needs:\n\n"
        response += "• What industry is your business in?\n"
        response += "• What's the main challenge you're trying to solve?\n"
        response += "• Are you looking for ways to save time, reduce costs, improve customer experience, or something else?\n\n"
        response += "With a bit more context, I can provide much more targeted and useful recommendations!"
        
        context["conversation_stage"] = "needs_assessment"
        return response


# Initialize the conversational bot
conversational_bot = ConversationalBot()

def fuzzy_match(phrase, keywords, cutoff=0.7):
    """Enhanced fuzzy matching that works with multi-word phrases"""
    phrase_lower = phrase.lower()
    
    # Try exact matches first
    for keyword in keywords:
        if keyword.lower() in phrase_lower:
            return keyword
    
    # Try individual words in the phrase
    for word in phrase_lower.split():
        match = get_close_matches(word, [k.lower() for k in keywords], n=1, cutoff=cutoff)
        if match:
            # Return the original keyword that matched
            for keyword in keywords:
                if keyword.lower() == match[0]:
                    return keyword
    
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
            "conversation_stage": "initial",
            "user_industry": None,
            "user_interests": [],
            "context_data": {}
        }
    
    context = session_context[session_id]
    context["conversation_history"].append({
        "message": user_message,
        "timestamp": datetime.now().isoformat()
    })
    
    # Keep conversation history manageable
    if len(context["conversation_history"]) > 20:
        context["conversation_history"] = context["conversation_history"][-15:]
    
    # Generate intelligent response
    reply = conversational_bot.generate_contextual_response(user_message, context)
    
    # Save chat to database
    try:
        chat_message = ChatMessage.objects.create(
            user_message=user_message,
            bot_reply=reply,
            session_id=session_id
        )
        serializer = ChatMessageSerializer(chat_message)
        chat_data = serializer.data
    except Exception as e:
        # Handle database errors gracefully
        chat_data = {
            "user_message": user_message,
            "bot_reply": reply,
            "session_id": session_id,
            "timestamp": datetime.now().isoformat()
        }

    return Response({
        "response": reply,
        "session_id": session_id,
        "chat": chat_data,
        "conversation_stage": context.get("conversation_stage", "unknown")
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_chat_history(request, session_id):
    try:
        messages = ChatMessage.objects.filter(session_id=session_id).order_by('timestamp')
        if not messages.exists():
            return Response({"error": "No chat history found for this session."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ChatMessageSerializer(messages, many=True)
        return Response({
            "chat_history": serializer.data,
            "session_context": session_context.get(session_id, {})
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": "Error retrieving chat history."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def clear_session(request, session_id):
    """Clear session context and optionally chat history"""
    try:
        # Clear session context
        if session_id in session_context:
            del session_context[session_id]
        
        # Optionally clear database history
        clear_db = request.query_params.get('clear_database', 'false').lower() == 'true'
        if clear_db:
            ChatMessage.objects.filter(session_id=session_id).delete()
        
        return Response({"message": "Session cleared successfully."}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": "Error clearing session."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_session_stats(request, session_id):
    """Get session statistics and context"""
    try:
        context = session_context.get(session_id, {})
        message_count = ChatMessage.objects.filter(session_id=session_id).count()
        
        return Response({
            "session_id": session_id,
            "message_count": message_count,
            "conversation_stage": context.get("conversation_stage", "initial"),
            "last_topic": context.get("last_topic"),
            "user_industry": context.get("user_industry"),
            "session_active": session_id in session_context
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": "Error retrieving session stats."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ChatMessageListCreateView(generics.ListCreateAPIView):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        session_id = self.request.query_params.get('session_id')
        if session_id:
            queryset = queryset.filter(session_id=session_id)
        return queryset.order_by('-timestamp')[:50]  # Limit to recent messages