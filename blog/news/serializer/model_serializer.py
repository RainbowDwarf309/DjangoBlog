from rest_framework import serializers
from news.models import Post, Category, Tag, User, UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser']


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['user', 'avatar', 'bio', 'first_name', 'last_name', 'email', 'karma', 'monthly_karma']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['title', 'slug', 'photo', 'get_absolute_url']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['title', 'slug']


class PostSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['title', 'slug', 'author', 'category', 'photo', 'content', 'created_at', 'updated_at',
                  'get_absolute_url', 'is_published', 'views', 'status', 'likes', 'dislikes', 'rating', 'tags']
