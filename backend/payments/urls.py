from django.urls import path
from .views import (
    StripeCheckoutSessionView, 
    MpesaPaymentRequestView, 
    MpesaCallbackView,
    MpesaPaymentStatusView
)

urlpatterns = [
    path('stripe-checkout/', StripeCheckoutSessionView.as_view(), name='stripe-checkout'),
    path('mpesa-payment/', MpesaPaymentRequestView.as_view(), name='mpesa-payment'),
    path('mpesa-callback/', MpesaCallbackView.as_view(), name='mpesa-callback'),
    path('mpesa-status/<int:payment_id>/', MpesaPaymentStatusView.as_view(), name='mpesa-status'),
]