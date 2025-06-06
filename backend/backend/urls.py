# backend/backend/urls.py
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.conf import settings
from django.conf.urls.static import static

def test_api(request):
    return JsonResponse({"message": "Hello from Django!"})

def root_view(request):
    return JsonResponse({
        "status": "Backend is running",
        "endpoints": [
            "/api/test/",
            "/api/portfolio/",
            "/api/enquiry/",
            "/api/chat/",
            "/api/requests/", 
            "/api/payments/",
            "/api/users/", 
        ]
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', root_view),
    path('api/test/', test_api),
    path('api/portfolio/', include('portfolio.urls')),
    path('api/enquiry/', include('enquiry.urls')),
    path('api/chat/', include('chat.urls')),
    path('api/requests/', include('project_requests.urls')), # Confirmed this refers to project_requests
    path('api/payments/', include('payments.urls')),
    path('api/users/', include('users.urls')), # ADDED: Include URLs from the users app
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # ADDED: Serve media files in development