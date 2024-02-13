from django.urls import path
from .views import RegistrationView, LoginView, ActivationView, UserListView, LogoutView, RegistrationPhoneView, ResetPasswordConfirmView, ResetPasswordConfirmView, ResetPasswordView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


urlpatterns = [
    path('register/', RegistrationView.as_view(), name = 'registration'),
    path('activate/', ActivationView.as_view()),
    path('login/', LoginView.as_view(), name = 'login'),
    path('refresh/', TokenRefreshView.as_view()),
    path('list_users/', UserListView.as_view()),
    path('logout/', LogoutView.as_view(), name = 'logout'),
    path('register_phone/', RegistrationPhoneView.as_view()),
    path('reset-password/', ResetPasswordView.as_view()),
    path('reset-password/confirm/', ResetPasswordConfirmView.as_view()),
    path('access/', TokenObtainPairView.as_view()),
    path('token-verify/', TokenVerifyView.as_view()),
    
]