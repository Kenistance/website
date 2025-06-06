from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from portfolio.models import Project
from .utils import create_stripe_checkout_session, create_mpesa_payment_request, verify_mpesa_payment
from .serializers import PaymentSerializer
from .models import Payment
import logging
import json

logger = logging.getLogger('payments')


class StripeCheckoutSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        project_id = request.data.get('project_id')
        user = request.user

        if not project_id:
            return Response({"success": False, "error": "Project ID is required"}, status=400)

        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response({"success": False, "error": "Project not found"}, status=404)

        if not project.requires_payment:
            return Response({"success": False, "error": "Project does not require payment"}, status=400)

        logger.info(f"Creating Stripe session for user {user.id}, project {project_id}")

        session_url = create_stripe_checkout_session(project, user)

        if session_url:
            payment = Payment.objects.create(
                user=user,
                project=project,
                amount=project.price,
                method='stripe',
                status='pending'
            )
            serializer = PaymentSerializer(payment)
            logger.info(f"Stripe payment record created: {payment.id}")
            return Response({
                "success": True,
                "checkout_url": session_url,
                "payment": serializer.data
            })
        else:
            return Response({"success": False, "error": "Failed to create Stripe session"}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class MpesaPaymentRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            project_id = request.data.get('project_id')
            phone_number = request.data.get('phone_number')
            user = request.user

            logger.info(f"M-Pesa payment request from user {user.id} for project {project_id}")

            if not project_id:
                return Response({"success": False, "error": "Project ID is required"}, status=400)

            if not phone_number:
                return Response({"success": False, "error": "Phone number is required"}, status=400)

            phone_number = phone_number.strip()
            phone_digits = ''.join(filter(str.isdigit, phone_number))

            if phone_digits.startswith('0') and len(phone_digits) == 10:
                phone_number = '254' + phone_digits[1:]
            elif phone_digits.startswith('254') and len(phone_digits) == 12:
                phone_number = phone_digits
            elif phone_digits.startswith('7') and len(phone_digits) == 9:
                phone_number = '254' + phone_digits
            else:
                return Response({
                    "success": False,
                    "error": "Invalid phone number format",
                    "errorMessage": "Please enter a valid Kenyan phone number (e.g., 0712345678 or 254712345678)"
                }, status=400)

            try:
                project = Project.objects.get(id=project_id)
            except Project.DoesNotExist:
                return Response({"success": False, "error": "Project not found"}, status=404)

            if not project.requires_payment:
                return Response({"success": False, "error": "Project does not require payment"}, status=400)

            logger.info(f"Processing M-Pesa payment: user={user.id}, project={project_id}, phone={phone_number}")

            # Create pending payment record
            payment = Payment.objects.create(
                user=user,
                project=project,
                amount=project.price,
                method='mpesa',
                status='pending'
            )

            response_data = create_mpesa_payment_request(
                phone_number=phone_number,
                amount=float(project.price),
                project_id=project.id,
                user_id=user.id
            )

            logger.info(f"M-Pesa API response: {response_data}")

            if response_data.get('success'):
                payment.transaction_id = response_data.get('checkoutRequestID', '')
                payment.save()
                serializer = PaymentSerializer(payment)
                return Response({
                    "success": True,
                    "payment": serializer.data,
                    "message": "M-Pesa request sent"
                })
            else:
                payment.delete()
                return Response({
                    "success": False,
                    "error": response_data.get('error', 'M-Pesa payment failed'),
                    "details": response_data.get('details', '')
                }, status=500)

        except Exception as e:
            logger.exception("Unexpected error in MpesaPaymentRequestView")
            return Response({
                "success": False,
                "error": "Server error while processing payment",
                "details": str(e)
            }, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class MpesaCallbackView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        callback_data = request.data
        logger.info(f"M-Pesa callback received: {json.dumps(callback_data, indent=2)}")

        try:
            # Parse M-Pesa callback data structure
            stk_callback = callback_data.get('Body', {}).get('stkCallback', {})
            
            if not stk_callback:
                logger.error("Invalid callback format - no stkCallback found")
                return Response({"ResultCode": 1, "ResultDesc": "Invalid callback format"})
            
            checkout_request_id = stk_callback.get('CheckoutRequestID')
            result_code = stk_callback.get('ResultCode')
            result_desc = stk_callback.get('ResultDesc')
            
            logger.info(f"Callback details: CheckoutRequestID={checkout_request_id}, ResultCode={result_code}")
            
            if not checkout_request_id:
                logger.error("No CheckoutRequestID in callback")
                return Response({"ResultCode": 1, "ResultDesc": "No CheckoutRequestID"})

            # Find the payment record
            try:
                payment = Payment.objects.get(
                    transaction_id=checkout_request_id,
                    method='mpesa'
                )
            except Payment.DoesNotExist:
                logger.error(f"Payment record not found for CheckoutRequestID: {checkout_request_id}")
                return Response({"ResultCode": 1, "ResultDesc": "Payment record not found"})

            # Update payment status based on result code
            if result_code == 0:
                # Payment successful
                payment.status = 'completed'
                
                # Extract additional payment details if available
                callback_metadata = stk_callback.get('CallbackMetadata', {})
                items = callback_metadata.get('Item', [])
                
                for item in items:
                    if item.get('Name') == 'MpesaReceiptNumber':
                        # Store the M-Pesa receipt number as transaction ID
                        payment.transaction_id = item.get('Value', checkout_request_id)
                        break
                
                logger.info(f"Payment {payment.id} marked as completed")
                
            elif result_code == 1032:
                # Payment cancelled by user
                payment.status = 'failed'
                logger.info(f"Payment {payment.id} cancelled by user")
                
            else:
                # Payment failed
                payment.status = 'failed'
                logger.info(f"Payment {payment.id} failed with result code: {result_code}")

            payment.save()
            
            return Response({
                "ResultCode": 0,
                "ResultDesc": "Callback processed successfully"
            })
            
        except Exception as e:
            logger.error(f"Error processing M-Pesa callback: {e}")
            return Response({
                "ResultCode": 1,
                "ResultDesc": f"Error processing callback: {str(e)}"
            })


class MpesaPaymentStatusView(APIView):
    """
    View to check the status of an M-Pesa payment
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, payment_id):
        try:
            payment = Payment.objects.get(id=payment_id, user=request.user, method='mpesa')
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found"}, status=404)

        # If payment is still pending, try to verify with M-Pesa
        if payment.status == 'pending' and payment.transaction_id:
            verification_result = verify_mpesa_payment(payment.transaction_id)
            
            if verification_result.get('success'):
                result_code = verification_result.get('result_code')
                if result_code == '0':
                    payment.status = 'completed'
                    payment.save()
                elif result_code in ['1032', '1037']:  # Cancelled or failed
                    payment.status = 'failed'
                    payment.save()

        serializer = PaymentSerializer(payment)
        return Response(serializer.data)