from .models import PayedAddress
from rest_framework import serializers

class CheckoutSerializer(serializers.ModelSerializer):
    # Предположим, что поле price связано с каким-то другим объектом, откуда можно получить цену
    price = serializers.IntegerField(source='price.some_field', default=100)
    
    class Meta:
        model = PayedAddress
        fields = ("full_name", "email", "street_address", "apartment_address", "country", "zip", "price")
