from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import EnquirySerializer

class EnquiryCreateView(APIView):
    def post(self, request):
        serializer = EnquirySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Enquiry submitted successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
