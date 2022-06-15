from django.urls import path
from .views import CheckoutAPIView

urlpatterns = [
    path('checkout/<int:id>', CheckoutAPIView.as_view())
]