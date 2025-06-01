from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from portfolio.models import Project
from .utils import create_stripe_checkout_session, create_mpesa_payment_request

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
            return Response({"checkout_url": session_url})
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

        response = create_mpesa_payment_request(phone_number, project.price, project.id, user.id)
        return Response(response)
