# backend/payments/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from portfolio.models import Project
from .utils import create_mpesa_payment_request, verify_mpesa_payment, create_stripe_checkout_session # Added create_stripe_checkout_session
from .serializers import PaymentSerializer
from .models import Payment
import logging
import json
from django.http import JsonResponse
from django.shortcuts import redirect # Added redirect

logger = logging.getLogger('payments')

@method_decorator(csrf_exempt, name='dispatch')
class MpesaPaymentRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Log the incoming request for debugging
            logger.info(f"M-Pesa payment request received")
            logger.info(f"Request data: {request.data}")
            logger.info(f"Request user: {request.user}")
            logger.info(f"User authenticated: {request.user.is_authenticated}")
            
            # Extract data
            project_id = request.data.get('project_id')
            phone_number = request.data.get('phone_number')
            user = request.user

            # Validate required fields
            if not project_id:
                logger.error("Missing project_id")
                return Response({
                    "success": False, 
                    "error": "Project ID is required",
                    "errorMessage": "Project ID is required"
                }, status=400)

            if not phone_number:
                logger.error("Missing phone_number")
                return Response({
                    "success": False, 
                    "error": "Phone number is required",
                    "errorMessage": "Phone number is required"
                }, status=400)

            # Validate and format phone number
            phone_number = phone_number.strip()
            phone_digits = ''.join(filter(str.isdigit, phone_number))
            
            logger.info(f"Original phone: {phone_number}, Digits only: {phone_digits}")

            if phone_digits.startswith('0') and len(phone_digits) == 10:
                phone_number = '254' + phone_digits[1:]
            elif phone_digits.startswith('254') and len(phone_digits) == 12:
                phone_number = phone_digits
            elif phone_digits.startswith('7') and len(phone_digits) == 9:
                phone_number = '254' + phone_digits
            else:
                logger.error(f"Invalid phone format: {phone_digits}")
                return Response({
                    "success": False,
                    "error": "Invalid phone number format",
                    "errorMessage": "Please enter a valid Kenyan phone number (e.g., 0712345678 or 254712345678)"
                }, status=400)

            logger.info(f"Formatted phone number: {phone_number}")

            # Validate project exists
            try:
                project = Project.objects.get(id=project_id)
                logger.info(f"Project found: {project.title}, Price: {project.price}, Requires payment: {project.requires_payment}")
            except Project.DoesNotExist:
                logger.error(f"Project not found: {project_id}")
                return Response({
                    "success": False, 
                    "error": "Project not found",
                    "errorMessage": "Project not found"
                }, status=404)

            if not project.requires_payment:
                logger.error(f"Project {project_id} doesn't require payment")
                return Response({
                    "success": False, 
                    "error": "Project does not require payment",
                    "errorMessage": "This project is free to download"
                }, status=400)

            # Create pending payment record first
            logger.info(f"Creating payment record for user {user.id}, project {project_id}")
            
            payment = Payment.objects.create(
                user=user,
                project=project,
                amount=project.price,
                method='mpesa',
                status='pending'
            )
            
            logger.info(f"Payment record created with ID: {payment.id}")

            # Make M-Pesa API request
            logger.info(f"Calling create_mpesa_payment_request")
            response_data = create_mpesa_payment_request(
                phone_number=phone_number,
                amount=float(project.price),
                project_id=project.id,
                user_id=user.id
            )

            logger.info(f"M-Pesa API response received: {response_data}")

            if response_data.get('success'):
                # Update payment with transaction ID
                checkout_request_id = response_data.get('checkoutRequestID')
                if checkout_request_id:
                    payment.transaction_id = checkout_request_id
                    payment.save()
                    logger.info(f"Payment {payment.id} updated with transaction_id: {checkout_request_id}")

                serializer = PaymentSerializer(payment)
                return Response({
                    "success": True,
                    "payment": serializer.data,
                    "message": response_data.get('message', 'M-Pesa payment request sent successfully'),
                    "checkoutRequestID": checkout_request_id
                })
            else:
                # Delete the payment record if M-Pesa request failed
                logger.error(f"M-Pesa request failed, deleting payment record {payment.id}")
                payment.delete()
                
                error_msg = response_data.get('errorMessage', response_data.get('error', 'M-Pesa payment request failed'))
                
                return Response({
                    "success": False,
                    "error": response_data.get('error', 'M-Pesa payment failed'),
                    "errorMessage": error_msg
                }, status=400)

        except Exception as e:
            logger.exception(f"Unexpected error in MpesaPaymentRequestView: {str(e)}")
            
            # Make sure we always return JSON
            return Response({
                "success": False,
                "error": f"Server error: {str(e)}",
                "errorMessage": "An unexpected error occurred. Please try again."
            }, status=500)

    def dispatch(self, request, *args, **kwargs):
        """Override dispatch to ensure we always return JSON responses"""
        try:
            response = super().dispatch(request, *args, **kwargs)
            logger.info(f"Response status: {response.status_code}")
            return response
        except Exception as e:
            logger.exception(f"Error in dispatch: {str(e)}")
            # Always return JSON even if there's an unexpected error
            return JsonResponse({
                "success": False,
                "error": f"Dispatch error: {str(e)}",
                "errorMessage": "An unexpected error occurred. Please try again."
            }, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class StripeCheckoutSessionView(APIView):
    permission_classes = [IsAuthenticated] # Ensures only authenticated users can access

    def post(self, request):
        try:
            logger.info(f"Stripe checkout session request received")
            logger.info(f"Request data: {request.data}")
            logger.info(f"Request user: {request.user}")
            logger.info(f"User authenticated: {request.user.is_authenticated}")

            project_id = request.data.get('project_id')
            user = request.user

            if not project_id:
                logger.error("Missing project_id for Stripe checkout")
                return Response({
                    "success": False,
                    "error": "Project ID is required",
                    "errorMessage": "Project ID is required for Stripe checkout"
                }, status=400)

            try:
                project = Project.objects.get(id=project_id)
                logger.info(f"Project found for Stripe: {project.title}, Price: {project.price}, Requires payment: {project.requires_payment}")
            except Project.DoesNotExist:
                logger.error(f"Project not found for Stripe: {project_id}")
                return Response({
                    "success": False,
                    "error": "Project not found",
                    "errorMessage": "Project not found for Stripe checkout"
                }, status=404)

            if not project.requires_payment:
                logger.error(f"Project {project_id} doesn't require payment for Stripe")
                return Response({
                    "success": False,
                    "error": "Project does not require payment",
                    "errorMessage": "This project is free to download, no Stripe payment needed"
                }, status=400)
            
            # Create a pending payment record
            logger.info(f"Creating pending Stripe payment record for user {user.id}, project {project_id}")
            payment = Payment.objects.create(
                user=user,
                project=project,
                amount=project.price,
                method='stripe',
                status='pending'
            )
            logger.info(f"Payment record created for Stripe with ID: {payment.id}")

            # Call the utility function to create the Stripe checkout session
            checkout_session_url = create_stripe_checkout_session(project, user)
            
            if checkout_session_url:
                logger.info(f"Stripe Checkout Session created: {checkout_session_url}")
                # Update the payment record with Stripe checkout session ID if available (optional, but good for tracking)
                # Note: Stripe Checkout Session ID is different from transaction ID after successful payment
                # You might want to update `payment.transaction_id` in your Stripe webhook handler.
                # For now, we'll redirect.
                return Response({
                    "success": True,
                    "redirect_url": checkout_session_url,
                    "message": "Stripe checkout session created successfully."
                }, status=200)
            else:
                logger.error(f"Failed to create Stripe Checkout Session for project {project_id}")
                # Delete the pending payment record if session creation failed
                payment.delete()
                return Response({
                    "success": False,
                    "error": "Failed to create Stripe checkout session",
                    "errorMessage": "Could not initiate Stripe payment. Please try again."
                }, status=500)

        except Exception as e:
            logger.exception(f"Unexpected error in StripeCheckoutSessionView: {str(e)}")
            return Response({
                "success": False,
                "error": f"Server error: {str(e)}",
                "errorMessage": "An unexpected error occurred during Stripe checkout. Please try again."
            }, status=500)