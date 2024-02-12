from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse
from django.views import View
import stripe
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from .serializers import CheckoutSerializer
from django.shortcuts import redirect

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION


class CheckoutView(APIView):
    @swagger_auto_schema(request_body=CheckoutSerializer)
    def post(self, request):
        session_data = {
            "mode": "payment",
            "success_url": "http://127.0.0.1:8000/pay/success/",
            "cancel_url": "http://127.0.0.1:8000/pay/cancel/",
            "line_items": [{
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": "test"
                    },
                    "unit_amount": 1000,  # Amount in cents, adjust as necessary
                },
                "quantity": 1,
            }],
        }

        session_data["client_reference_id"] = '1'
        session = stripe.checkout.Session.create(**session_data)
        
        return redirect(session.url, code=303)
        

class PaymentSuccessView(APIView):
    def get(self, request):
        return JsonResponse({'message': 'Оплата прошла успешно'})

class PaymentCancelView(APIView):
    def get(self, request):
        return JsonResponse({'message': 'Оплата отменена'})






