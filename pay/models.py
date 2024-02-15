from django.db import models
from django.contrib.auth import get_user_model
from teachers.models import Post

User = get_user_model()

class PayedAddress(models.Model):
    full_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = models.CharField(max_length=100, blank=True, null=True)
    zip = models.CharField(max_length=100, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    price = models.ForeignKey(Post, on_delete=models.CASCADE, null=False)
    
    def __str__(self):
        return f'PayedAddress {str(self.id)}'
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    pay_address = models.ForeignKey(PayedAddress, on_delete=models.CASCADE, blank=True, null=True)
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'Order {str(self.id)}'
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    course = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True) 
    price = models.DecimalField(max_digits=9, decimal_places=2)
    quantity = models.IntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    
    def __str__(self):
        return f'OrderItem {str(self.id)}'
