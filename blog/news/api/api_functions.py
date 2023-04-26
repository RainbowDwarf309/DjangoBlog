import datetime
import logging

from news.models import ActionTrack, Comment, Post
from django.http import HttpRequest, JsonResponse
from services.functions import get_client_ip, track_action

logger = logging.getLogger('process')


def check_object_id(object_id: int) -> int:
    """Check if object id is number and grater than 0"""
    object_id = int(object_id.strip())
    assert object_id > 0
    return object_id


def check_post_status(request: HttpRequest, post_object: Post) -> JsonResponse:
    """Verifies post status, if post is deleted returns JsonResponse."""
    if post_object.status == Post.AttrStatus.DELETED:
        response = JsonResponse({'error': 'Sorry, post deleted.'})
        response.status_code = 400
        logger.info(f'Block get_post_view_api. Return 400={response}, from ip={get_client_ip(request)}')
        return response


def post_already_viewed_today(request: HttpRequest, post_id: int) -> bool:
    """If user viewed post today returns True, otherwise returns False"""
    action_user_post_already_viewed_today = ActionTrack.objects.filter(
        action=ActionTrack.AttrAction.POST_VIEW,
        details=f'ip={get_client_ip(request)}, code_id={post_id} viewed').order_by('date')
    if action_user_post_already_viewed_today.exists():
        return action_user_post_already_viewed_today.last().date.date() == datetime.datetime.today().date()
    else:
        return False


def post_viewed(request: HttpRequest, post_object: Post, post_id: int, action: HttpRequest,
                user_post_already_viewed_today: bool) -> JsonResponse:
    """
    Checks if the post has been viewed today.

    If user didn't view post today, then count of views increases by 1, otherwise track_action will make record
    that post already viewed.

    Args:
        post_object (Post): Class of the object on which the operation will be performed.
        post_id (int): The id of the object on which the action will be performed.
        action (HttpRequest): Depending on the specified action, the relevant operation will be performed on the object.
        user_post_already_viewed_today (bool): True if user viewed the post today, otherwise False
    """
    if not user_post_already_viewed_today:
        post_object.views += 1
        post_object.save()
        track_action(request=request, action=ActionTrack.AttrAction.POST_VIEW,
                     page=ActionTrack.AttrPage.API_POST,
                     details=f'ip={get_client_ip(request)}, code_id={post_id} viewed')
        logger.info(f'Block get_post_view_api. post views +=1, post id={post_id},'
                    f' ip={get_client_ip(request)}')
        response = JsonResponse({'rate': post_object.rating, 'views': post_object.views, 'state': 'viewed'})
        response.status_code = 200
        return response
    else:
        track_action(request=request, action=ActionTrack.AttrAction.POST_VIEW,
                     page=ActionTrack.AttrPage.API_POST,
                     action_reason=ActionTrack.AttrReason.POST_ALREADY_VIEWED,
                     details=f'from ip={get_client_ip(request)}, code_id={post_id}')
        logger.debug(f'Block get_post_view_api Post views change unsuccessfully. Already viewed today. '
                     f'action={action}, from ip={get_client_ip(request)}')
        response = JsonResponse({'rate': post_object.rating, 'views': post_object.views, 'state': 'Already viewed'})
        response.status_code = 200
        return response


def post_change_rating(request: HttpRequest, post_object: Post, post_id: int, action: HttpRequest,
                       user_changed_utility: ActionTrack) -> JsonResponse:
    """
    Change post utility.

    If user has never rated a post, then depending on the action post's utility changes to Like or Dislike.

    Args:
        post_object (Post): Class of the object on which the operation will be performed.
        post_id (int): The id of the object on which the action will be performed.
        action (HttpRequest): Depending on the specified action, the relevant operation will be performed on the object.
        user_changed_utility (ActionTrack): Variable containing information about an object.

    Returns:
        JsonResponse with HTTP 200 if everything's OK.
        JsonResponse with HTTP 400 if function get unexpected action.
    """
    if action == 'like' and not user_changed_utility:

        post_object.set_like_or_dislike(is_like=True)
        post_object.save()
        track_action(request=request, action=ActionTrack.AttrAction.POST_RATING_PLUS,
                     page=ActionTrack.AttrPage.API_POST,
                     details=f'ip={get_client_ip(request)}, code_id={post_id}, u')
        logger.info(f'Block get_post_view_api. Post utility change +=1, post id= {post_id}, '
                    f'from ip={get_client_ip(request)}')
        response = JsonResponse({'rate': post_object.rating, 'views': post_object.views})
        response.status_code = 200
        return response
    elif action == 'dislike' and not user_changed_utility:
        post_object.set_like_or_dislike(is_dislike=True)
        post_object.save()
        track_action(request=request, action=ActionTrack.AttrAction.POST_RATING_MINUS,
                     page=ActionTrack.AttrPage.API_POST,
                     details=f'ip={get_client_ip(request)}, code_id={post_id}, u')
        logger.info(f'Block get_post_view_api. Post utility change -=1, code_id={post_id}, '
                    f'from ip={get_client_ip(request)}')
        response = JsonResponse({'rate': post_object.rating, 'views': post_object.views})
        response.status_code = 200
        return response
    elif action and user_changed_utility:
        track_action(request=request, action_reason=ActionTrack.AttrReason.POST_RATING_ALREADY_CHANGED,
                     page=ActionTrack.AttrPage.API_POST,
                     action=ActionTrack.AttrAction.POST_RATING_MINUS if action == 'dislike' else
                     ActionTrack.AttrAction.POST_RATING_PLUS)
        logger.debug(f'Block get_post_view_api Post utility change unsuccessfully user_changed_utility, '
                     f'post id={post_id}, from ip={get_client_ip(request)}')
        response = JsonResponse({'rate': post_object.rating, 'views': post_object.views,
                                 'error': 'Already changed.'})
        response.status_code = 200
        return response
    else:
        response = JsonResponse({'error': 'Unexpected action.'})
        response.status_code = 400
        logger.info(f'Block get_post_view_api Post change unsuccessfully, unexpected action.'
                    f'action={action}, from ip={get_client_ip(request)}')
        return response


def check_comment_status(request: HttpRequest, comment_object: Comment) -> JsonResponse:
    """Verifies coupon status. If comment is invisible or deleted, then returns relevant JsonResponse."""
    if comment_object.status == Comment.AttrStatus.INVISIBLE:
        response = JsonResponse({'error': 'Sorry, comment invalid.'})
        response.status_code = 400
        logger.debug(f'Block coupon_utility_change_api. Return 400={response}, from ip={get_client_ip(request)}')
        return response
    else:
        response = JsonResponse({'error': 'Sorry, comment deleted.'})
        response.status_code = 400
        logger.debug(f'Block coupon_utility_change_api. Return 400={response}, from ip={get_client_ip(request)}')
        return response
