import logging
from news.models import ActionTrack, Post, Comment, Category
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from django.http import HttpRequest, JsonResponse

from news.api.api_functions import (
    check_object_id,
    get_client_ip,
    check_post_status,
    check_comment_status,
    post_already_viewed_today,
    post_viewed,
    post_change_rating,
    track_action,
)

logger = logging.getLogger('process')


def get_post_view_api(request: HttpRequest) -> JsonResponse:
    """Change the number of views or rating of the post"""
    post_id = request.GET.get('code_id', None)
    action = request.GET.get('action', None)
    try:
        post_id = check_object_id(post_id)
        post = Post.objects.get(pk=post_id)
        user_changed_utility = ActionTrack.objects.filter(details=f'ip={get_client_ip(request)}, '
                                                                  f'code_id={post_id}, u')
        if post.status != Post.AttrStatus.APPROVED:
            return check_post_status(request, post)
        user_post_already_viewed_today = post_already_viewed_today(request, post_id)
    except (ValueError, TypeError, AssertionError):
        response = JsonResponse({'error': 'code_id must be integer or string of integer, and more or equal 0.'})
        response.status_code = 400
        logger.info(f'Block get_post_view_api. Return 400={response}')
        return response
    except ObjectDoesNotExist:
        response = JsonResponse({'error': 'Object with code_id=' + str(post_id) + " does not exist."})
        response.status_code = 400
        logger.info(f'Block get_post_view_api. Return 400={response}, from ip={get_client_ip(request)}')
        return response
    except Exception as e:
        response = JsonResponse({'error': 'Unexpected error'})
        response.status_code = 400
        logger.warning(f'Block get_post_view_api. Return 400={response}, from ip={get_client_ip(request)}, '
                       f'Exc:{e}')
        return response
    else:
        if action == 'viewed' and not user_changed_utility:
            return post_viewed(request, post, post_id, action, user_post_already_viewed_today)
        else:
            return post_change_rating(request, post, post_id, action, user_changed_utility)


@login_required
def get_favorites_view_api(request, **kwargs) -> JsonResponse:
    slug = request.GET.get('slug', "")
    try:
        model = kwargs['model']
        object_model = kwargs['object_model']
        user = request.user
        my_object = object_model.objects.all().get(slug=slug)
        model.add_or_delete_favorite(user=user, obj=my_object)
        model_fav = {
            Post: user.favoritepost,
            Category: user.favoritecategory
        }
    except KeyError:
        response = JsonResponse({'error': 'Please specify the correct model and object_model'})
        response.status_code = 400
    except ObjectDoesNotExist:
        response = JsonResponse(
            {'error': f"Object with slug:{slug!r} does not exist. Please specify the correct slug"})
        response.status_code = 400
    except Exception:
        response = JsonResponse({'error': 'Unexpected error'})
        response.status_code = 400
    else:
        if model_fav[object_model].filter(obj=my_object.pk).exists():
            response = JsonResponse({'status': 'Successful', 'state': 'added'})
        else:
            response = JsonResponse({'status': 'Successful', 'state': 'deleted'})
        response.status_code = 200
    return response


@login_required
def get_post_like_or_dislike_view_api(request: HttpRequest) -> JsonResponse:
    slug = request.GET.get('slug', "")
    action = request.GET.get('action', "")
    try:
        obj = Post.objects.get(slug=slug)
        user_changed_utility = ActionTrack.objects.filter(details=f'ip={get_client_ip(request)}, '
                                                                  f'code_id={obj.pk}, u')
        if obj.status != Post.AttrStatus.APPROVED:
            return check_post_status(request, obj)
        if action == 'like' and not user_changed_utility:
            obj.set_like_or_dislike(is_like=True)
            obj.save()
            track_action(request=request, action=ActionTrack.AttrAction.POST_RATING_PLUS,
                         page=ActionTrack.AttrPage.API_LIKE_DISLIKE,
                         details=f'ip={get_client_ip(request)}, code_id={obj.pk}, u')
            response = JsonResponse({'status': 'Successful', 'state': 'like', 'rate': obj.rating, 'views': obj.views})
            response.status_code = 200
            return response
        elif action == 'dislike' and not user_changed_utility:
            obj.set_like_or_dislike(is_dislike=True)
            obj.save()
            track_action(request=request, action=ActionTrack.AttrAction.POST_RATING_MINUS,
                         page=ActionTrack.AttrPage.API_LIKE_DISLIKE,
                         details=f'ip={get_client_ip(request)}, code_id={obj.pk}, u')
            response = JsonResponse(
                {'status': 'Successful', 'state': 'dislike', 'rate': obj.rating, 'views': obj.views}
            )
            response.status_code = 200
            return response
        elif action and user_changed_utility:
            track_action(request=request, action_reason=ActionTrack.AttrReason.POST_RATING_ALREADY_CHANGED,
                         page=ActionTrack.AttrPage.API_LIKE_DISLIKE,
                         action=ActionTrack.AttrAction.POST_RATING_MINUS if action == 'dislike' else
                         ActionTrack.AttrAction.POST_RATING_PLUS)
            logger.debug(f'Block get_post_like_or_dislike_view_api Post rating change unsuccessfully '
                         f'user_changed_utility, post id={obj.pk}, from ip={get_client_ip(request)}')
            response = JsonResponse({'rate': obj.rating, 'views': obj.views,
                                     'error': 'You already set like or dislike.'})
            response.status_code = 200
            return response
    except ObjectDoesNotExist:
        response = JsonResponse(
            {'error': f"Object with slug:{slug!r} does not exist. Please specify the correct slug"})
        response.status_code = 400
        return response
    except Exception:
        response = JsonResponse({'error': 'Unexpected error'})
        response.status_code = 400
        return response
    else:
        response = JsonResponse({'error': 'Unexpected action.'})
        response.status_code = 400
        return response


@login_required
def get_comment_like_or_dislike_view_api(request: HttpRequest) -> JsonResponse:
    code_id = request.GET.get('code_id', "")
    action = request.GET.get('action', "")
    try:
        object_pk = check_object_id(code_id)
        obj = Comment.objects.get(pk=object_pk)
        user_changed_utility = ActionTrack.objects.filter(details=f'ip={get_client_ip(request)}, '
                                                                  f'code_id={obj.pk}, u')
        if obj.status != Comment.AttrStatus.VISIBLE:
            return check_comment_status(request, obj)
        if action == 'like' and not user_changed_utility:
            obj.set_like_or_dislike(is_like=True)
            obj.save()
            track_action(request=request, action=ActionTrack.AttrAction.COMMENT_RATING_PLUS,
                         page=ActionTrack.AttrPage.API_COMMENT_RATING,
                         details=f'ip={get_client_ip(request)}, code_id={obj.pk}, u')
            response = JsonResponse({'status': 'Successful', 'state': 'like', 'rate': obj.rating})
            response.status_code = 200
            return response
        elif action == 'dislike' and not user_changed_utility:
            obj.set_like_or_dislike(is_dislike=True)
            obj.save()
            track_action(request=request, action=ActionTrack.AttrAction.COMMENT_RATING_MINUS,
                         page=ActionTrack.AttrPage.API_COMMENT_RATING,
                         details=f'ip={get_client_ip(request)}, code_id={obj.pk}, u')
            response = JsonResponse({'status': 'Successful', 'state': 'dislike', 'rate': obj.rating})
            response.status_code = 200
            return response
        elif action and user_changed_utility:
            track_action(request=request, action_reason=ActionTrack.AttrReason.COMMENT_RATING_ALREADY_CHANGED,
                         page=ActionTrack.AttrPage.API_COMMENT_RATING,
                         action=ActionTrack.AttrAction.COMMENT_RATING_MINUS if action == 'dislike' else
                         ActionTrack.AttrAction.COMMENT_RATING_PLUS)
            logger.debug(f'Block get_comment_like_or_dislike_view_api Comment rating change unsuccessfully '
                         f'user_changed_utility, post id={obj.pk}, from ip={get_client_ip(request)}')
            response = JsonResponse({'rate': obj.rating, 'error': 'You already set like or dislike.'})
            response.status_code = 200
            return response
    except ObjectDoesNotExist:
        response = JsonResponse(
            {'error': f"Object with code_id:{code_id!r} does not exist. Please specify the correct code_id"})
        response.status_code = 400
        return response
    except Exception:
        response = JsonResponse({'error': 'Unexpected error'})
        response.status_code = 400
        return response
    else:
        response = JsonResponse({'error': 'Unexpected action.'})
        response.status_code = 400
        return response
