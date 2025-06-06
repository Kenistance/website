# backend/payments/views.py - Complete version with M-Pesa, Stripe and error handling

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from portfolio.models import Project
from .utils import (
    create_mpesa_payment_request, 
    verify_mpesa_payment, 
    create_stripe_checkout_session,
    get_mpesa_access_token # Needed for MpesaCallbackView
)
from .serializers import PaymentSerializer
from .models import Payment
import logging
import json
from django.http import JsonResponse
from django.shortcuts import redirect # Needed for Stripe redirects
from django.conf import settings # Needed for callback URL

logger = logging.getLogger('payments')

@method_decorator(csrf_exempt, name='dispatch')
class MpesaPaymentRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            logger.info(f"M-Pesa payment request received")
            logger.info(f"Request data: {request.data}")
            logger.info(f"Request user: {request.user}")
            logger.info(f"User authenticated: {request.user.is_authenticated}")
            
            project_id = request.data.get('project_id')
            phone_number = request.data.get('phone_number')
            user = request.user

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

            logger.info(f"Creating payment record for user {user.id}, project {project_id}")
            
            payment = Payment.objects.create(
                user=user,
                project=project,
                amount=project.price,
                method='mpesa',
                status='pending'
            )
            
            logger.info(f"Payment record created with ID: {payment.id}")

            logger.info(f"Calling create_mpesa_payment_request")
            response_data = create_mpesa_payment_request(
                phone_number=phone_number,
                amount=float(project.price),
                project_id=project.id,
                user_id=user.id
            )

            logger.info(f"M-Pesa API response received: {response_data}")

            if response_data.get('success'):
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
            return JsonResponse({
                "success": False,
                "error": f"Dispatch error: {str(e)}",
                "errorMessage": "An unexpected error occurred. Please try again."
            }, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class StripeCheckoutSessionView(APIView):
    permission_classes = [IsAuthenticated]

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
            
            logger.info(f"Creating pending Stripe payment record for user {user.id}, project {project_id}")
            payment = Payment.objects.create(
                user=user,
                project=project,
                amount=project.price,
                method='stripe',
                status='pending'
            )
            logger.info(f"Payment record created for Stripe with ID: {payment.id}")

            checkout_session_url = create_stripe_checkout_session(project, user)
            
            if checkout_session_url:
                logger.info(f"Stripe Checkout Session created: {checkout_session_url}")
                return Response({
                    "success": True,
                    "redirect_url": checkout_session_url,
                    "message": "Stripe checkout session created successfully."
                }, status=200)
            else:
                logger.error(f"Failed to create Stripe Checkout Session for project {project_id}")
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


@method_decorator(csrf_exempt, name='dispatch')
class MpesaCallbackView(APIView):
    permission_classes = [AllowAny] # M-Pesa callbacks don't have authentication

    def post(self, request):
        logger.info(f"M-Pesa Callback received")
        logger.info(f"Callback data: {json.dumps(request.data, indent=2)}")

        try:
            callback_data = request.data
            body = callback_data.get('Body', {})
            stk_callback = body.get('stkCallback', {})

            merchant_request_id = stk_callback.get('MerchantRequestID')
            checkout_request_id = stk_callback.get('CheckoutRequestID')
            result_code = stk_callback.get('ResultCode')
            result_desc = stk_callback.get('ResultDesc')
            
            logger.info(f"Callback - MerchantRequestID: {merchant_request_id}, CheckoutRequestID: {checkout_request_id}, ResultCode: {result_code}")

            if checkout_request_id:
                try:
                    payment = Payment.objects.get(transaction_id=checkout_request_id, status='pending', method='mpesa')
                    logger.info(f"Found pending M-Pesa payment record: {payment.id}")

                    if str(result_code) == '0':
                        # Payment was successful
                        callback_metadata = stk_callback.get('CallbackMetadata', {})
                        item = next((item for item in callback_metadata.get('Item', []) if item.get('Name') == 'MpesaReceiptNumber'), None)
                        mpesa_receipt_number = item.get('Value') if item else None

                        if mpesa_receipt_number:
                            payment.status = 'completed'
                            payment.transaction_id = mpesa_receipt_number # Update with actual M-Pesa receipt
                            payment.save()
                            logger.info(f"Payment {payment.id} completed. MpesaReceiptNumber: {mpesa_receipt_number}")
                            # Here you would typically trigger product delivery or access for the user
                            # e.g., send confirmation email, unlock download
                        else:
                            payment.status = 'failed'
                            payment.save()
                            logger.warning(f"Payment {payment.id} failed: MpesaReceiptNumber not found in successful callback.")
                        
                    else:
                        # Payment failed or was cancelled
                        payment.status = 'failed'
                        payment.save()
                        logger.warning(f"Payment {payment.id} failed with ResultCode: {result_code}, ResultDesc: {result_desc}")

                    return JsonResponse({"ResultCode": "0", "ResultDesc": "Callback received successfully"}, status=200)

                except Payment.DoesNotExist:
                    logger.error(f"No pending M-Pesa payment found for CheckoutRequestID: {checkout_request_id}")
                    return JsonResponse({"ResultCode": "1", "ResultDesc": "Payment record not found"}, status=404)
            else:
                logger.error("M-Pesa Callback: CheckoutRequestID is missing")
                return JsonResponse({"ResultCode": "1", "ResultDesc": "Missing CheckoutRequestID"}, status=400)

        except Exception as e:
            logger.exception(f"Error processing M-Pesa callback: {str(e)}")
            return JsonResponse({"ResultCode": "1", "ResultDesc": f"Internal server error: {str(e)}"}, status=500)


class MpesaPaymentStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, payment_id):
        try:
            payment = Payment.objects.get(id=payment_id, user=request.user)
            serializer = PaymentSerializer(payment)
            
            # Optionally, you can add logic here to query Safaricom for the latest status
            # of pending transactions if needed, using payment.transaction_id (CheckoutRequestID)
            if payment.status == 'pending' and payment.method == 'mpesa' and payment.transaction_id:
                logger.info(f"Querying M-Pesa for status of payment {payment.id} with CheckoutRequestID: {payment.transaction_id}")
                status_response = verify_mpesa_payment(payment.transaction_id)
                logger.info(f"M-Pesa status query response: {status_response}")

                if status_response.get('success'):
                    result_code = status_response.get('result_code')
                    if result_code == '0':
                        # Payment is truly successful
                        payment.status = 'completed'
                        # Safaricom status query might not return MpesaReceiptNumber directly here
                        # It's better to get it from the callback.
                        payment.save()
                        logger.info(f"Payment {payment.id} status updated to completed after direct query.")
                        serializer = PaymentSerializer(payment) # Reserialize to get updated status
                    elif result_code == '1032': # Transaction cancelled by user
                        payment.status = 'failed'
                        payment.save()
                        logger.info(f"Payment {payment.id} cancelled by user (ResultCode 1032).")
                        serializer = PaymentSerializer(payment)
                    elif result_code == '2001': # Transaction not found (can indicate failure or pending)
                        # No change in status, still pending, wait for callback
                        logger.info(f"Payment {payment.id} still pending or not found on M-Pesa (ResultCode 2001).")
                    else:
                        # Other failure codes
                        payment.status = 'failed'
                        payment.save()
                        logger.warning(f"Payment {payment.id} failed with M-Pesa ResultCode: {result_code}.")
                        serializer = PaymentSerializer(payment)
                else:
                    logger.error(f"Failed to query M-Pesa for payment {payment.id} status: {status_response.get('error')}")

            return Response({
                "success": True,
                "payment": serializer.data
            }, status=200)

        except Payment.DoesNotExist:
            logger.error(f"Payment record not found for ID: {payment_id} and user {request.user.id}")
            return Response({
                "success": False,
                "error": "Payment not found",
                "errorMessage": "The requested payment record does not exist or you do not have permission to view it."
            }, status=404)
        except Exception as e:
            logger.exception(f"Error getting M-Pesa payment status for payment {payment_id}: {str(e)}")
            return Response({
                "success": False,
                "error": f"Server error: {str(e)}",
                "errorMessage": "An unexpected error occurred while retrieving payment status. Please try again."
            }, status=500)