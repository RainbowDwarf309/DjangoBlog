from django.urls import path
from django.contrib.auth import views

from .views import *
from .user_views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('post/<str:slug>', SinglePostView.as_view(), name='post'),
    path('category/<str:slug>', PostsByCategoryView.as_view(), name='category'),
    path('tag/<str:slug>', PostsByTagView.as_view(), name='tag'),
    path('create_post', CreatePostView.as_view(), name='create_post'),
    path('registration/', SignUpView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/settings/', UserProfilePlatformView.as_view(), name='user_profile_settings'),
    path('search_posts/', SearchPostView.as_view(), name='search'),
]
