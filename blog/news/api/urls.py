from django.urls import path

from . import api_views

from news.models import Post, FavoritePost, FavoriteCategory, Category

urlpatterns = [
    path('code_id/', api_views.get_post_view_api, name='ajax_post'),
    path('favorite_post/', api_views.get_favorites_view_api,
         kwargs={'model': FavoritePost, 'object_model': Post}, name='ajax_favorite_post'),
    path('favorite_category/', api_views.get_favorites_view_api,
         kwargs={'model': FavoriteCategory, 'object_model': Category}, name='ajax_favorite_category'),
    path('post_like_dislike/', api_views.get_post_like_or_dislike_view_api, name='ajax_post_like_dislike'),
    path('comment_like_dislike/', api_views.get_comment_like_or_dislike_view_api, name='ajax_comment_like_dislike'),
]
