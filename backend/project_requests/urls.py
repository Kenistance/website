from django.urls import path
from .views import ProjectRequestList

urlpatterns = [
    path('requests/', ProjectRequestList.as_view(), name='project-requests'),
]
