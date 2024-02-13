from rest_framework import serializers
from django.db.models import Avg

from .models import Post, PostImages, Review, Favorite, Rating
from category.models import LanguageCategory, PriceCategory


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImages
        fields = '__all__'


class FavoriteSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source = 'owner.id')
    owner_username = serializers.ReadOnlyField(source = 'owner.username')

    class Meta:
        model = Favorite
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['post_name'] = instance.post.name
        if instance.post.preview:
            preview = instance.post.preview
            representation['post_preview'] = preview.url
        else:
            representation['post_preview'] = None
        return representation


class PostListSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source='owner.username')
    language_category_name = serializers.ReadOnlyField(source = 'language_category.name')
    price_category = serializers.ReadOnlyField(source = 'price_category.price_range')


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['quantity_of_favorites'] = instance.favorites.count()
        representation['quantity_of_reviews'] = instance.reviews.count()

        ratings = instance.ratings.all()
        if ratings.exists():
            average_rating = ratings.aggregate(Avg('rating'))['rating__avg']
            representation['average_rating'] = round(average_rating, 2)
            representation['quantity_of_ratings'] = instance.ratings.count()
        else:
            representation['average_rating'] = None
            representation['quantity_of_ratings'] = 0

        request = self.context.get('request')
        category_slug = request.query_params.get('category_slug', None)
        if category_slug:
            posts = instance.teachers.filter(language_category__slug=category_slug)
            representation['posts'] = PostListSerializer(posts, many=True, context=self.context).data

        return representation

    class Meta:
        model = Post
        fields = ('id', 'name', 'owner', 'owner_username', 'language_category_name', 'price', 'price_category', 'preview')


class PostCreateSerializer(serializers.ModelSerializer):
    images = PostImageSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = ('name', 'description', 'preview', 'language_category', 'price', 'price_category', 'images')

    def create(self, validated_data):
        request = self.context.get('request')
        images_data = validated_data.pop('images', None)
        language_category = validated_data.pop('language_category')
        price_category = validated_data.pop('price_category')
        price = validated_data.pop('price')

        post = Post.objects.create(language_category=language_category, price_category=price_category, price=price, **validated_data)

        if images_data:
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
    def is_favorite(post, user):
        return user.favorites.filter(post=post).exists()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user = self.context['request'].user
        
        representation['favorites'] = FavoriteSerializer(instance.favorites.all(), many=True).data
        representation['Quantity of favorites'] = len(representation['favorites'])

        representation['Review'] = ReviewSerializer(instance.reviews.all(), many=True).data
        representation['Quantity of reviews'] = instance.reviews.count()
        
        ratings = instance.ratings.all()
        if ratings.exists():
            average_rating = ratings.aggregate(Avg('rating'))['rating__avg']
            representation['ratings'] = RatingSerializer(ratings, many=True).data
            representation['average_rating'] = round(average_rating, 2)
        else:
            representation['ratings'] = []
            representation['average_rating'] = None

        if user.is_authenticated:
            representation['is_favorite'] = self.is_favorite(instance, user)
        return representation

    
class ReviewSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source = 'owner.id')
    commentator_username = serializers.ReadOnlyField(source = 'owner.username')

    class Meta:
        model = Review
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['post_name'] = instance.post.name
        if instance.post.preview:
            preview = instance.post.preview
            representation['post_preview'] = preview.url
        else:
            representation['post_preview'] = None
        return representation
    
class ReviewActionSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source = 'owner.id')
    commentator_username = serializers.ReadOnlyField(source = 'owner.username')
    post = serializers.CharField(required = False)

    class Meta:
        model = Review
        fields = '__all__'

    def create(self, validated_data):
        post = self.context.get('post')
        post = Post.objects.get(pk = post)
        validated_data['post'] = post
        owner = self.context.get('owner')
        validated_data['owner'] = owner
        return super().create(validated_data)
    
from rest_framework import serializers
from .models import Rating

class RatingSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source = 'owner.email')
    post = serializers.ReadOnlyField(source = 'post.name')

    class Meta:
        model = Rating
        fields = '__all__'
    
