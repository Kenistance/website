from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import FileResponse, Http404
from django.conf import settings
import os

from .models import Project
from .serializers import ProjectSerializer


class ProjectListView(APIView):
    def get(self, request):
        projects = Project.objects.all().order_by('-created_at')
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)


class ProjectDownloadView(APIView):
    def get(self, request, pk):
        try:
            project = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404("Project not found")

        if project.requires_payment:
            return Response({"error": "Payment required for this file"}, status=status.HTTP_403_FORBIDDEN)

        # If there is a public download_url, redirect or return it
        if project.download_url:
            return Response({"download_url": project.download_url})

        # Otherwise try to serve from file_path internally
        if not project.file_path:
            return Response({"error": "File not available"}, status=status.HTTP_404_NOT_FOUND)

        full_path = os.path.join(settings.MEDIA_ROOT, project.file_path)

        if not os.path.exists(full_path):
            return Response({"error": "File does not exist on server"}, status=status.HTTP_404_NOT_FOUND)

        try:
            return FileResponse(open(full_path, 'rb'), as_attachment=True)
        except Exception:
            return Response({"error": "Unable to serve the file"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
