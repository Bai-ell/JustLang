import imp
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegistrationSerializer, ActivationSerializer, UserSerializer, RegistrationPhoneSerializer, ResetPasswordSerializer, ConfirmPasswordSerializer
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, get_object_or_404, ListAPIView
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import permissions
from justlang.tasks import send_confirmation_email_task, send_confirmation_password_task
from drf_yasg.utils import swagger_auto_schema
from .send_email import send_confirmation_email


User = get_user_model()

class ActivationView(GenericAPIView):
    serializer_class = ActivationSerializer()

    def get(self, request):
        code = request.GET.get('u')
        user = get_object_or_404(User, activation_code = code)
        user.is_active = True
        user.save()
        return Response('Успешно активирован', status=200)
    
    def post(self, request):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response('Успешно активирован!', status=200)
    
class   LoginView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)

class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message':'Logout successful'}, status=200)
        except Exception as e:
            return Response({'error':'Invalid Token'}, status=400)
                

class RegistrationView(APIView):
    @swagger_auto_schema(request_body=RegistrationSerializer())
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                try:
                    send_confirmation_email(user.email, user.activation_code)
                except:
                    
                    return Response({"message": "Зарегистрировался, но на почту код не отправился.",
                                    'data': serializer.data}, status=200)
            return Response({'message': 'User registered successfully'})
        else:
            return Response({'errors': serializer.errors})
                

class RegistrationPhoneView(APIView):
    def post(self, request):
        data = request.data
        serializer = RegistrationPhoneSerializer(data = data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Registered success', status=201)
    
class ResetPasswordView(APIView):
    def get(self, request):
        return Response({'message': 'Please provide an email to reset the password'})
    
    def post(self, request):
        serializer = ConfirmPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email = email)
                user.create_phone_number_code()
                user.save()
                # send_confirmation_password(user.email, user.activation_code)
                send_confirmation_password_task.delay(user.email, user.activation_code)
                return Response({'activation_code': user.activation_code}, status=200)
            except:
                return Response({'message': 'User with this email does not exist!'}, status=404)
        return Response(serializer.errors, status=400)
        
class ResetPasswordConfirmView(APIView):
    def post(self, request):
        code = request.GET.get('u')
        user = get_object_or_404(User, activation_code = code)
        serializer = ResetPasswordSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        new_password = serializer.validated_data['new_password']
        user.set_password(new_password)
        user.activation_code = ''
        user.save()
        return Response('Your password has been successfully updated', status=200)
    
class ResetPasswordView(APIView):
    def get(self, request):
        return Response({'message': 'Please provide an email to reset the password'})
    
    def post(self, request):
        serializer = ConfirmPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email = email)
                user.create_phone_number_code()
                user.save()
                # send_confirmation_password(user.email, user.activation_code)
                send_confirmation_password_task.delay(user.email, user.activation_code)
                return Response({'activation_code': user.activation_code}, status=200)
            except:
                return Response({'message': 'User with this email does not exist!'}, status=404)
        return Response(serializer.errors, status=400)