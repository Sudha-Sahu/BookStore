
from rest_framework import serializers
from .models import PlaceOrder


class CheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceOrder
        fields = ['address']

    address = serializers.CharField(max_length=300)

    