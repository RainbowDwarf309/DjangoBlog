from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from .model_serializer import PostSerializer, CategorySerializer, UserSerializer, UserProfileSerializer
from news.models import Post, Category, User, UserProfile
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny


class PostViewSet(ReadOnlyModelViewSet):
    queryset = Post.objects.filter(is_published=True)
    serializer_class = PostSerializer


class CategoryViewSet(ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailViewSet(ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        category = self.kwargs['category']
        return Post.objects.filter(is_published=True, category__slug=category)


class PostDetailViewSet(RetrieveAPIView):
    lookup_field = "slug"
    queryset = Post.objects.filter(is_published=True)
    serializer_class = PostSerializer


class UserViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class UserProfileViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAdminUser]


class UserProfileDetailViewSet(RetrieveAPIView):
    lookup_field = "user"
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]


class TagDetailViewSet(ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        tag = self.kwargs['tag']
        return Post.objects.filter(is_published=True, tags__slug=tag)
