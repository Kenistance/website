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
            "/api/payments/",   # Add payments here
        ]
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', root_view),
    path('api/test/', test_api),
    path('api/portfolio/', include('portfolio.urls')),
    path('api/enquiry/', include('enquiry.urls')), 
    path('api/chat/', include('chat.urls')),
    path('api/requests/', include('project_requests.urls')),
    path('api/payments/', include('payments.urls')),  # Payments URLs here
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
