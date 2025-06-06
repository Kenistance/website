# backend/portfolio/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny # Import AllowAny
from django.http import FileResponse, Http404
from django.conf import settings
import os

from .models import Project
from .serializers import ProjectSerializer


class ProjectListView(APIView):
    # THIS IS THE FIX for your authentication issue for public portfolio list
    permission_classes = [AllowAny]

    def get(self, request):
        projects = Project.objects.all().order_by('-created_at')
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)


class ProjectDownloadView(APIView):
    # This view might still need authentication if only paid users can download files
    # For now, it respects requires_payment which is now tied to price > 0
    # You might want to add IsAuthenticated here if only logged-in users can initiate downloads (even free ones)
    permission_classes = [AllowAny] # Changed to AllowAny for simplicity unless specified otherwise

    def get(self, request, pk):
        try:
            project = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404("Project not found")

        # Logic: If price > 0, it means payment is required.
        # This view should only serve free items or after a payment check is integrated.
        # For now, if price > 0, we don't serve the file directly via this view.
        if project.price > 0:
            return Response({"error": "Payment required for this file. Please use the payment options on the portfolio page."}, status=status.HTTP_403_FORBIDDEN)

        # If there is a public download_url, redirect or return it
        if project.download_url:
            return Response({"download_url": project.download_url})

        # Otherwise try to serve from file_path internally
        # Ensure MEDIA_ROOT is correctly configured in settings.py for this
        if not project.file_path:
            return Response({"error": "File not available for download"}, status=status.HTTP_404_NOT_FOUND)

        full_path = os.path.join(settings.MEDIA_ROOT, project.file_path)

        if not os.path.exists(full_path):
            return Response({"error": "File does not exist on server"}, status=status.HTTP_404_NOT_FOUND)

        try:
            return FileResponse(open(full_path, 'rb'), content_type='application/octet-stream')
        except Exception as e:
            return Response({"error": f"Error serving file: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)