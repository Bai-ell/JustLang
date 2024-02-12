from .models import Order, OrderItem, PaydAddress
from rest_framework import serializers
# from teachers.models import price_category


class CheckoutSerializer(serializers.ModelSerializer):
    price = serializers.IntegerField(default = 100)
    class Meta:
        model = PaydAddress
        fields = ("full_name","email","street_address","atartment_address","country","zip","price",)
        
    