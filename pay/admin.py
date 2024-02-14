from django.contrib import admin
from .models import Order, OrderItem, PayedAddress

admin.site.register(PayedAddress)
admin.site.register(OrderItem)
admin.site.register(Order)