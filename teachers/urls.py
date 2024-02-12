from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import PostListCreateView, PostDetailView

urlpatterns = [
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('posts/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/<slug:slug>/favorite/', PostListCreateView.favorite, name='post-favorite'),
    path('posts/<slug:slug>/comment/', PostListCreateView.comment, name='post-comment'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
