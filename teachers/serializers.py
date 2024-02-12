from rest_framework import serializers
from .models import Post, PostImages, Comment, Favorite
from category.models import Category
# from like.serializers import LikeSerializer
# from comment.serializers import CommentSerializer

class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImages
        fields = '__all__'


class PostListSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source='owner.username')
    language_category_name = serializers.ReadOnlyField(source = 'language_category.name')
    price_category = serializers.ReadOnlyField(source = 'price_category.price_range')


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['favorites'] = FavoriteSerializer(instance.favorites.all(), many=True).data
        representation['quantity_of_favorites'] = 0
        for _ in representation['favorites']:
            representation['quantity_of_favorites'] += 1
        return representation


    class Meta:
        model = Post
        fields = ('id', 'title', 'owner', 'language_category_name', 'price_category', 'preview', 'owner_username')


class PostCreateSerializer(serializers.ModelSerializer):
    images = PostImageSerializer(many=True, required=False)
    category = serializers.PrimaryKeyRelatedField(
        required = True, queryset = Category.objects.all()
    )

    class Meta:
        model = Post
        fields = ('title', 'body', 'preview', 'category','images')

    def create(self, validated_data):
        request = self.context.get('request')
        post = Post.objects.create(**validated_data)
        images_data = request.FILES.getlist('images')
        for image in images_data:
            PostImages.objects.create(images=image, post=post)
        return post


class PostDetailSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source='owner.username')
    category_name = serializers.ReadOnlyField(source='category.name')
    images = PostImageSerializer(many=True)

    class Meta:
        model = Post
        fields = '__all__'

    @staticmethod
    def is_liked(post, user):
        return user.likes.filter(post=post).exists()
    
    @staticmethod
    def is_favorite(post, user):
        return user.favorites.filter(post=post).exists()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['favorites'] = FavoriteSerializer(instance.likes.all(), many=True).data
        representation['Quantity of likes'] = 0
        for _ in representation['favorites']:
            representation['Quantity of favorites'] += 1
        user = self.context['request'].user
        representation['Comment'] = CommentSerializer(instance.comments.all(), many = True).data
        representation['Quantity of comments'] = instance.comments.count()
        if user.is_authenticated:
            representation['is_liked'] = self.is_liked(instance, user)
            representation['is_favorite'] = self.is_favorite(instance, user)
        return representation
    
class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source = 'owner.id')
    commentator_username = serializers.ReadOnlyField(source = 'owner.username')

    class Meta:
        model = Comment
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['post_title'] = instance.post.title
        if instance.post.preview:
            preview = instance.post.preview
            representation['post_preview'] = preview.url
        else:
            representation['post_preview'] = None
        return representation
    
class CommentActionSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source = 'owner.id')
    commentator_username = serializers.ReadOnlyField(source = 'owner.username')
    post = serializers.CharField(required = False)

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        post = self.context.get('post')
        post = Post.objects.get(pk = post)
        validated_data['post'] = post
        owner = self.context.get('owner')
        validated_data['owner'] = owner
        return super().create(validated_data)
    
class FavoriteSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source = 'owner.id')
    owner_username = serializers.ReadOnlyField(source = 'owner.username')

    class Meta:
        model = Favorite
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['post_title'] = instance.post.title
        if instance.post.preview:
            preview = instance.post.preview
            representation['post_preview'] = preview.url
        else:
            representation['post_preview'] = None
        return representation