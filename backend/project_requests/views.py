from rest_framework import generics
from .models import ProjectRequest
from .serializers import ProjectRequestSerializer

class ProjectRequestList(generics.ListAPIView):
    queryset = ProjectRequest.objects.all()
    serializer_class = ProjectRequestSerializer
