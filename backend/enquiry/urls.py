from django.urls import path
from .views import EnquiryCreateView

urlpatterns = [
    path('submit/', EnquiryCreateView.as_view(), name='enquiry-submit'),
]
