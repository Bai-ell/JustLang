from django.contrib import admin
from .models import Order, OrderItem, PaydAddress

admin.site.register(PaydAddress)
admin.site.register(OrderItem)
admin.site.register(Order)