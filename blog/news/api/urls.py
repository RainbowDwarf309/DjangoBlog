from django.urls import path

from . import api_views

from news.models import Post, FavoritePost

urlpatterns = [
    path('favorite_post/', api_views.get_favorites_view_api,
         kwargs={'model': FavoritePost, 'object_model': Post}, name='ajax_favorite_post'),
    path('post_like_dislike/', api_views.get_like_or_dislike_view_api, name='ajax_post_like_dislike'),
    path('comment_like_dislike/', api_views.get_comment_like_or_dislike_view_api, name='ajax_comment_like_dislike'),
]
