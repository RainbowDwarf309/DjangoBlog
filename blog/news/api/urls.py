from django.urls import path

from . import api_views

from news.models import Post, FavoritePost

urlpatterns = [
    path('favorite_post/', api_views.get_favorites_view_api,
         kwargs={'model': FavoritePost, 'object_model': Post}, name='ajax_favorite_post'),
]
