from django.urls import path
from .views import PaymentView, PaymentDetailView

urlpatterns = [
    path('', PaymentView.as_view(), name='payment-create'),
    path('<uuid:payment_id>', PaymentDetailView.as_view(), name='payment-detail'),
]
