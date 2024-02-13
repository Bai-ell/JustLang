from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import PostListCreateView, PostDetailView
from category.views import LanguageCategoryAPIView, PriceCategoryAPIView

urlpatterns = [
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('posts/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/<slug:slug>/favorite/', PostListCreateView.favorite, name='post-favorite'),
    path('posts/<slug:slug>/review/', PostListCreateView.review, name='post-review'),
    path('posts/<slug:slug>/ratings/', PostListCreateView.ratings, name='product-ratings'),
]


