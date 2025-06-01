from django.urls import path
from .views import ProjectListView, ProjectDownloadView

urlpatterns = [
    path('', ProjectListView.as_view(), name='project-list'),
    path('<int:pk>/download/', ProjectDownloadView.as_view(), name='project-download'),
]
