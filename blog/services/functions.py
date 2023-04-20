import logging
from news.models import ActionTrack, Post
from django.core.exceptions import ObjectDoesNotExist
from django.db import DataError
from typing import Union

logger = logging.getLogger('process')


def get_post_from_slug(self, slug='slug') -> Post | bool:
    try:
        return Post.objects.get(slug=self.kwargs[slug])
    except ObjectDoesNotExist:
        return False
    except Exception:
        return False


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
    except DataError as e:
        logger.error(f'Impossible to record IP {e=}')
    except Exception:
        logger.error('Track_action can\'t create new object', exc_info=True)
