from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .permissions import IsAuthor, IsAuthorOrAdmin
from rest_framework import generics, permissions
from rest_framework.decorators import action
import logging

from category.models import LanguageCategory, PriceCategory
from .models import Post, Favorite
from .serializers import PostListSerializer, PostCreateSerializer, PostDetailSerializer, FavoriteSerializer, ReviewSerializer, ReviewActionSerializer, RatingSerializer

logger = logging.getLogger(__name__)

class StandartPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
            },
            'count': self.page.paginator.count,
            'results': data
        })            

    
class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return PostCreateSerializer
        return PostListSerializer
    
    @action(['POST', 'DELETE', 'GET'], detail=True)
    def favorite(self, request, slug):  
        post = Post.objects.filter(slug=slug)
        user = request.user

        if request.method == 'POST':
            if user.favorites.filter(post=post).exists():
                return Response('This post is already added to favorites!', status=400)
            Favorite.objects.create(owner=user, post=post)
            return Response('Added to favorites', status=200)

        elif request.method == 'DELETE':
            favorite = user.favorites.filter(post=post)
            if favorite.exists():
                favorite.delete()
                return Response('Post successfully removed from favorites!')
            return Response('This post is not in favorites!', status=400)

        elif request.method == 'GET':
            favorites = user.favorites.all()
            serializer = FavoriteSerializer(instance=favorites, many=True)
            return Response(serializer.data, status=200)
        
        else:
            return Response('Method not allowed', status=405)

    @action(['GET', 'POST', 'DELETE'], detail=True)
    def review(self, request, slug):
        post = get_object_or_404(slug=slug)
        user = request.user
        if request.method == 'POST':
            serializer = ReviewActionSerializer(data=request.data, context={'post': post.id, 'owner': user})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=200)
        elif request.method == 'DELETE':
            review_slug = self.request.query_params.get('slug')
            review = post.reviews.filter(slug=review_slug)
            if review.exists():
                review.delete()
                return Response('The review has been deleted', status=204)
            return Response('Review not found!', status=404)
        else:
            reviews = post.reviews.all()
            serializer = ReviewSerializer(instance=reviews, many=True)
            if not reviews:
                return Response('No reviews found for this post', status=404)
            return Response(serializer.data, status=200)
        
    @action(['GET', "POST", 'DELETE'], detail=True)
    def ratings(self, request, slug):
        product = get_object_or_404(Post, slug=slug)
        user = request.user

        if request.method == 'GET':
            rating = product.ratings.all()
            serializer = RatingSerializer(instance=rating, many=True)
            logger.info(f'Get request for ratings of teacher {slug} by user {user}')
            return Response(serializer.data, status=200)
        
        elif request.method == 'POST':
            if product.ratings.filter(owner=user).exists():
                return Response('Вы уже поставили оценку этому учителю!', status=400)
            serializer = RatingSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(owner=user, product=product)
            logger.info(f'Post request for ratings of product {slug} by user {user}')
            return Response(serializer.data, status=201)
        
        else:
            if not product.ratings.filter(owner=user).exists():   
                return Response('Вы не можете удалить оценку так как вы её не оставляли', status=400)
            rating = product.ratings.get(owner=user)
            rating.delete()
            logger.critical(f'Delete request for ratings of product {slug} by user {user}')
            return Response('Вы успешно удалили оценку!', status=204)
        
class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    lookup_field = 'slug'

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return (IsAuthorOrAdmin(),)
        elif self.request.method in ['PUT', 'PATCH']:
            return (IsAuthor(),)
        return [permissions.AllowAny()]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return PostCreateSerializer
        return PostDetailSerializer
