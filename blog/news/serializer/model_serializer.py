from rest_framework import serializers
from news.models import Post, Category


class PostSerializer(serializers.ModelSerializer):
    absolute_url = serializers.SerializerMethodField()
    category_slug = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    @staticmethod
    def get_absolute_url(obj):
        return obj.get_absolute_url()

    @staticmethod
    def get_category_slug(obj):
        return obj.category.slug


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
