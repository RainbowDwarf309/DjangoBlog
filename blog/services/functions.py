import logging
from news.models import ActionTrack, Post, User, Comment, Newsletter, NewsType
from django.core.exceptions import ObjectDoesNotExist
from django.db import DataError
from typing import Union, List
from django.db.models import QuerySet
from services.redis_functions import _redis_get_summary_profile_data, _redis_set_summary_profile_data, \
    redis_get_popular_posts_of_day, redis_get_popular_posts_of_week
from datetime import datetime
import json

from news import karma

logger = logging.getLogger('process')


def get_param_from_request(request, param) -> Union[str, None]:
    """ HTTP_REFERER HTTP_USER_AGENT REMOTE_HOST"""
    return request.META.get(param) if request.META.get(param) else None


def get_session_key(request) -> Union[str, None]:
    return request.session.session_key if request.session.session_key else None


def get_client_ip(request) -> str:
    x_forwarded_for = get_param_from_request(request, 'HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    else:
        return request.META.get('REMOTE_ADDR')


def track_action(request, page: ActionTrack.AttrPage, action: ActionTrack.AttrAction, details: str = None,
                 action_reason: ActionTrack.AttrReason = None) -> None:
    """
    Create record into ActionTrack model

    User_status can be omitted if the object is passed.
    Object type is determined automatically.
    """

    try:
        action_object = ActionTrack.objects.create(
            ip=get_client_ip(request),
            http_referer=get_param_from_request(request, 'HTTP_REFERER'),
            session_key=get_session_key(request),
            user_agent=get_param_from_request(request, 'HTTP_USER_AGENT'),

            page=page,
            page_url=request.get_full_path(),
            action=action,

            action_reason=action_reason,
            details=details,
        )

        if request.user.is_anonymous:
            user_status = ActionTrack.AttrUserStatus.ANONYMOUS
        elif request.user.is_staff:
            user_status = ActionTrack.AttrUserStatus.STAFF
        else:
            action_object.user = request.user
            user_status = ActionTrack.AttrUserStatus.JUST_USER

        action_object.user_status = user_status
        action_object.save()

        if not request.user.is_anonymous \
                and not ActionTrack.objects.filter(user=action_object.user,
                                                   date__date=datetime.today()).exists():
            karma.everyday_bonus(action_object.user)
            ActionTrack.objects.create(user=action_object.user, action=ActionTrack.AttrAction.EVERYDAY_KARMA_GIVEN,
                                       page=page)

    except DataError as e:
        logger.error(f'Impossible to record IP {e=}')
    except Exception:
        logger.error('Track_action can\'t create new object', exc_info=True)


def create_summary_profile_data(user: User) -> dict:
    posts = Post.objects.filter(author=user)
    comments = Comment.objects.filter(user_submitter=user)
    posts_total_views = get_posts_total_views(posts)
    return {
        'posts_count': posts.count(),
        'posts_approved_count': posts.filter(status=Post.AttrStatus.APPROVED).count(),
        'posts_deleted_count': posts.filter(status=Post.AttrStatus.DELETED).count(),
        'posts_like_dislike': get_posts_like_dislike_ratio(posts),
        'comments_like_and_dislike': get_comments_like_dislike_ratio(comments),
        'comments_count': comments.count(),
        'posts_total_views': posts_total_views,
        'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M'),
    }


def get_summary_profile_data(user: User) -> dict:
    cache_key = str(user.pk) + '-summary_profile_data'
    result = _redis_get_summary_profile_data(cache_key)
    if result:
        return json.loads(result)
    else:
        data = create_summary_profile_data(user)
        _redis_set_summary_profile_data(cache_key, data)
    return data


def get_posts_like_dislike_ratio(posts) -> float:
    """Returns average percentage like/dislike ratio(0.0-100.00) of posts"""
    posts_likes = sum((post.likes for post in posts.exclude(status=Post.AttrStatus.DELETED)))
    posts_dislikes = sum((post.dislikes for post in posts.exclude(status=Post.AttrStatus.DELETED)))
    if posts_dislikes == 0:
        return 100 if posts_likes != 0 else 50
    return round((posts_likes / (posts_dislikes + posts_likes)) * 100, 2)


def get_comments_like_dislike_ratio(comments) -> float:
    """Returns average percentage like/dislike ratio(0.0-100.00) of comments."""
    comments_likes = sum((comment.count_of_likes for comment in comments))
    comments_dislikes = sum((comment.count_of_dislikes for comment in comments))
    if comments_dislikes == 0:
        return 100 if comments_likes != 0 else 50
    return round((comments_likes / (comments_dislikes + comments_likes)) * 100, 2)


def get_posts_total_views(posts) -> int:
    """Returns the sum of all views on all posts"""
    posts_total_views = sum([post.views for post in posts])
    return 1 if posts_total_views == 0 else posts_total_views


def get_top_contributors_for_all_time():
    return User.objects.filter(is_staff=False).order_by('-userprofile__karma')[:10]


def get_top_contributors_for_last_month():
    return User.objects.filter(is_staff=False).order_by('-userprofile__monthly_karma')[:10]


def get_type_of_news() -> dict:
    type_of_news = NewsType.objects.all()[::1]
    types_list = []
    for types in type_of_news:
        types_list.append(types.type_of_news)
    return dict([(types, []) for types in types_list])


def get_active_newsletter_subscribers() -> dict:
    active_subscribers = Newsletter.objects.filter(is_subscribed=True)
    type_of_news = get_type_of_news()
    for subscriber in active_subscribers:
        choices = subscriber.choices.all()[::1]
        for choice in choices:
            type_of_news.setdefault(choice.type_of_news, []).append(subscriber.email)
    return type_of_news


def get_popular_posts_of_day() -> QuerySet:
    redis_posts = redis_get_popular_posts_of_day()
    return Post.objects.filter(pk__in=redis_posts.keys())


def get_popular_posts_of_week() -> QuerySet:
    redis_posts = redis_get_popular_posts_of_week()
    return Post.objects.filter(pk__in=redis_posts.keys())
