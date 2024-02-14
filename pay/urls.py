from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    # path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('success/', views.PaymentSuccessView.as_view(), name='PaymentSuccess'),
    path('cancel/', views.PaymentCancelView.as_view(), name='PaymentCancel'),
]
