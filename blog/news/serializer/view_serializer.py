from django.template.defaultfilters import slugify
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .model_serializer import PostSerializer, CategorySerializer, UserSerializer, UserProfileSerializer, TagSerializer, \
    PostCreateSerializer
from news.models import Post, Category, User, UserProfile, Tag
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework import status


class PostViewSet(ReadOnlyModelViewSet):
    queryset = Post.objects.filter(is_published=True)
    serializer_class = PostSerializer


class CategoryViewSet(ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


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


class PostCreateView(APIView):
    serializer_class = PostCreateSerializer
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        data = request.data
        try:
            token = Token.objects.get(key=data["author"])
            user_id = token.user.id
            data["author"] = user_id
        except Exception:
            return Response({
                "error": "Invalid token"
            }, status=status.HTTP_400_BAD_REQUEST)

        data["slug"] = slugify(data["title"])
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
