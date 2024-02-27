from django.urls import include, path
from django.contrib.auth import views
from news.authentication.authentication import LoginViewDRF, LogoutViewDRF, RegisterView
from news.serializer.view_serializer import PostViewSet, CategoryViewSet, PostDetailViewSet, CategoryDetailViewSet, \
    UserViewSet, UserProfileViewSet, UserProfileDetailViewSet, TagDetailViewSet, PostCreateView, TagViewSet

from .views import *
from .user_views import *

urlpatterns = [
    # Django views for delete in future
    path('', HomeView.as_view(), name='home'),  # done
    path('post/<str:slug>', SinglePostView.as_view(), name='post'),  # done
    path('author/<int:pk>', PostsByAuthorView.as_view(), name='author'),
    path('category/<str:slug>', PostsByCategoryView.as_view(), name='category'),  # done
    path('categories_list/', CategoriesListView.as_view(), name='categories_list'),  # done
    path('tag/<str:slug>', PostsByTagView.as_view(), name='tag'),
    path('create_post', CreatePostView.as_view(), name='create_post'),
    path('registration/', SignUpView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/settings/', UserProfilePlatformView.as_view(), name='user_profile_settings'),
    path('community/', CommunityView.as_view(), name='community'),
    path('profile/summary/', UserProfileSummaryView.as_view(), name='user_profile_summary'),
    path('profile/publications/', UserProfilePublicationsView.as_view(), name='user_profile_publications'),
    path('search_posts/', SearchPostView.as_view(), name='search'),
    path('change_email/<uidb64>/<token>/', ActivateAccountView.as_view(), name='account_activation_confirm'),
    path('change_email/', ChangeEmailView.as_view(), name='change_email'),
    path('change_password/', UserPasswordChangeView.as_view(), name='change_password'),
    path('password_change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    # DRF API
    path('posts/', PostViewSet.as_view({'get': 'list'}), name='posts'),
    path('post_detail/<str:slug>/', PostDetailViewSet.as_view(), name='post_detail'),
    path('category_detail/<slug:category>/', CategoryDetailViewSet.as_view(), name='category_detail'),
    path('categories/', CategoryViewSet.as_view({'get': 'list'}), name='categories'),
    path('tag_detail/<slug:tag>/', TagDetailViewSet.as_view(), name='tag_detail'),
    path('tags/', TagViewSet.as_view({'get': 'list'}), name='tags'),
    path('users/', UserViewSet.as_view({'get': 'list'}), name='users'),
    path('user_profiles/', UserProfileViewSet.as_view({'get': 'list'}), name='user_profiles'),
    path('user_profile_detail/<str:token>/', UserProfileDetailViewSet.as_view(), name='user_profile_detail'),
    path('logins/', LoginViewDRF.as_view(), name='logins'),  # TODO: update later url and view name and add token
    path('logouts/', LogoutViewDRF.as_view(), name='logouts'),  # TODO: update later url and view name
    path('registrations/', RegisterView.as_view(), name='register'),  # TODO: update later url and view name
    path('posts_create/', PostCreateView.as_view(), name='post_create'),

    # TODO: ChangeEmailViewSet
    # TODO: ChangePasswordViewSet
    # TODO: UserProfilePlatformViewSet
    # TODO: UserProfileSummaryViewSet
    # TODO: UserProfilePublicationsViewSet
    # TODO: CommunityViewSet
    # TODO: SearchPostViewSet
    # TODO: ActivateAccountViewSet
    # TODO: PopularPostsViewSet
    # TODO: JWT

    # API
    path('ajax/', include('news.api.urls')),
]
