from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from portfolio.models import Project
from .utils import create_stripe_checkout_session, create_mpesa_payment_request
from .serializers import PaymentSerializer
from .models import Payment


class StripeCheckoutSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        project_id = request.data.get('project_id')
        user = request.user

        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response({"error": "Project not found"}, status=404)

        if not project.requires_payment:
            return Response({"error": "Project does not require payment"}, status=400)

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
            return Response({
                "checkout_url": session_url,
                "payment": serializer.data
            })
        else:
            return Response({"error": "Failed to create Stripe session"}, status=500)


class MpesaPaymentRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        project_id = request.data.get('project_id')
        phone_number = request.data.get('phone_number')
        user = request.user

        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response({"error": "Project not found"}, status=404)

        if not project.requires_payment:
            return Response({"error": "Project does not require payment"}, status=400)

        response_data = create_mpesa_payment_request(
            phone_number=phone_number,
            amount=project.price,
            project_id=project.id,
            user_id=user.id
        )

        if response_data.get('success'):
            payment = Payment.objects.create(
                user=user,
                project=project,
                amount=project.price,
                method='mpesa',
                status='pending',
                transaction_id=response_data.get('transaction_id', '')
            )
            serializer = PaymentSerializer(payment)
            response_data['payment'] = serializer.data

        return Response(response_data)


class MpesaCallbackView(APIView):
    permission_classes = [AllowAny]  # Safely allow external API (e.g. Safaricom) to POST

    def post(self, request):
        callback_data = request.data

        transaction_id = callback_data.get('transaction_id')
        status = callback_data.get('status')
        metadata = callback_data.get('metadata', {})
        project_id = metadata.get('project_id')
        user_id = metadata.get('user_id')

        try:
            payment = Payment.objects.get(
                transaction_id=transaction_id,
                project_id=project_id,
                user_id=user_id,
                method='mpesa'
            )
        except Payment.DoesNotExist:
            return Response({"error": "Payment record not found"}, status=404)

        if status == 'success':
            payment.status = 'completed'
        elif status == 'failed':
            payment.status = 'failed'
        else:
            payment.status = 'unknown'

        payment.save()
        return Response({"message": "Callback processed successfully"})
