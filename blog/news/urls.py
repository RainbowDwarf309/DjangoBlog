from django.urls import path
from django.contrib.auth import views

from .views import *
from .user_views import *

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('post/<str:slug>', SinglePost.as_view(), name='post'),
    path('category/<str:slug>', PostsByCategory.as_view(), name='category'),
    path('tag/<str:slug>', PostsByTag.as_view(), name='tag'),
    path('create_post', CreatePost.as_view(), name='create_post'),
    path('registration/', SignUpView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/settings/', UserProfilePlatformView.as_view(), name='user_profile_settings'),
]
