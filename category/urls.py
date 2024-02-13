from django.urls import path
from .views import LanguageCategoryAPIView, PriceCategoryAPIView

urlpatterns = [
    # URL для LanguageCategoryAPIView
    path('language-categories/', LanguageCategoryAPIView.as_view(), name='language-category-list'),
    path('language-categories/<slug:slug>/', LanguageCategoryAPIView.as_view(), name='language-category-detail'),

    # URL для PriceCategoryAPIView
    path('price-categories/', PriceCategoryAPIView.as_view(), name='price-category-list'),
    path('price-categories/<slug:slug>/', PriceCategoryAPIView.as_view(), name='price-category-detail'),
]
