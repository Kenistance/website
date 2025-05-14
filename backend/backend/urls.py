from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def test_api(request):
    return JsonResponse({"message": "Hello from Django!"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/test/', test_api),
    path('api/portfolio/', include('portfolio.urls')),
    path('api/enquiry/', include('enquiry.urls')), 
    path('api/chat/', include('chat.urls')),
]
