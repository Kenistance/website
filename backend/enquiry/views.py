from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from .serializers import EnquirySerializer

class EnquiryCreateView(APIView):
    def post(self, request):
        serializer = EnquirySerializer(data=request.data)
        if serializer.is_valid():
            enquiry = serializer.save()

            # Compose and send the email
            send_mail(
                subject=f"📩 New Enquiry from {enquiry.name}",
                message=f"""
You have received a new enquiry:

Name: {enquiry.name}
Email: {enquiry.email}
Phone: {enquiry.phone}
Message:
{enquiry.message}
                """,
                from_email='kenkaarick@gmail.com',  # ✅ Matches EMAIL_HOST_USER in settings
                recipient_list=['kennedychomba797@gmail.com'],  # ✅ Your receiving inbox
                fail_silently=False,
            )

            return Response(
                {"message": "✅ Enquiry submitted and emailed successfully!"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
