from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .permissions import IsAuthor, IsAuthorOrAdmin
from rest_framework import generics, permissions
from rest_framework.decorators import action

from .models import Post, Favorite, Comment
from .serializers import PostListSerializer, PostCreateSerializer, PostDetailSerializer, FavoriteSerializer, CommentSerializer, CommentActionSerializer



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
    def favorite(self, request, pk):
        post = self.get_object()
        user = request.user
        if request.method == 'POST':
            if user.favorites.filter(post=post).exists():
                return Response('This post is already added to favorites!', status=400)
            Favorite.objects.create(owner=user, post=post)
            return Response('Added to favorites', status=201)
        elif request.method == 'DELETE':
            favorite = user.favorites.filter(post=post)
            if favorite.exists():
                favorite.delete()
                return Response('Post successfully removed from favorites!')
            return Response('This post is not in favorites!', status=400)
        else:
            favorites = user.favorites.all()
            serializer = FavoriteSerializer(instance=favorites, many=True)
            return Response(serializer.data, status=200)

    @action(['GET', 'POST', 'DELETE'], detail=True)
    def comment(self, request, pk):
        post = self.get_object()
        user = request.user
        if request.method == 'POST':
            serializer = CommentActionSerializer(data=request.data, context={'post': post.id, 'owner': user})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=200)
        elif request.method == 'DELETE':
            comment_id = self.request.query_params.get('id')
            comment = post.comments.filter(pk=comment_id)
            if comment.exists():
                comment.delete()
                return Response('The comment has been deleted', status=204)
            return Response('Comment not found!', status=404)
        else:
            comments = post.comments.all()
            serializer = CommentSerializer(instance=comments, many=True)
            if not comments:
                return Response('No comments found for this post', status=404)
            return Response(serializer.data, status=200)
        
class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    lookup_field = 'slug'

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return (IsAuthorOrAdmin(),)
        elif self.request.method in ['PUT', 'PATCH']:
            return (IsAuthor(),)
        return [permissions.AllowAny]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return PostCreateSerializer
        return PostDetailSerializer
