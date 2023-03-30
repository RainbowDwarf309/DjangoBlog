from django.urls import path
from django.contrib.auth import views

from .views import *
from .user_views import *

urlpatterns = [
    path('', Home.as_view(), name='home'),

    path('registration/', SignUpView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]
