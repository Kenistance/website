from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Project
from .serializers import ProjectSerializer

class ProjectListView(APIView):
    def get(self, request):
        projects = Project.objects.all().order_by('-created_at')
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)
