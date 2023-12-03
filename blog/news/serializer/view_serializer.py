from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from .model_serializer import PostSerializer, CategorySerializer
from news.models import Post, Category
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]


class CategoryViewSet(ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
