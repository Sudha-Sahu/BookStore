
from rest_framework import serializers


class CheckoutSerializer(serializers.ModelSerializer):
    address = serializers.CharField(max_length=300)

    