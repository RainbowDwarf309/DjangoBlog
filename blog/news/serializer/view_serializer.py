from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from .model_serializer import PostSerializer, CategorySerializer
from news.models import Post, Category
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny


class PostViewSet(ReadOnlyModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CategoryViewSet(ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class PostDetailViewSet(APIView):

    def get(self, slug):
        post = Post.objects.get(slug=slug)
        serializer = PostSerializer(post)
        return Response(serializer.data)
