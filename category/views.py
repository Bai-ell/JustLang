from django import views
from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .permissions import IsAdminUserOrReadOnly
from .models import LanguageCategory, PriceCategory
from .serializers import LanguageCategorySerializer, PriceCategorySerializer

class LanguageCategoryAPIView(APIView):
    permission_classes = [IsAdminUserOrReadOnly]

    def get(self, request, slug=None):
        if slug:
            category = get_object_or_404(LanguageCategory, slug=slug)
            serializer = LanguageCategorySerializer(category)
            return Response(serializer.data)
        else:
            categories = LanguageCategory.objects.all()
            serializer = LanguageCategorySerializer(categories, many=True)
            return Response(serializer.data, {"message": "Категория не найден!"})
        
    def post(self, request):
        serializer = LanguageCategorySerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
class PriceCategoryAPIView(APIView):
    permission_classes = [IsAdminUserOrReadOnly]

    def get(self, request, slug=None):
        if slug:
            category = get_object_or_404(PriceCategory, slug=slug)
            serializer = PriceCategorySerializer(category)
            return Response(serializer.data)
        else:
            categories = PriceCategory.objects.all()
            serializer = PriceCategorySerializer(categories, many=True)
            return Response(serializer.data, {"message": "Категория не найденa!"})
        
    def post(self, request):
        serializer = PriceCategorySerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)