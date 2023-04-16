from news.models import Post, Comment
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from django.http import JsonResponse


@login_required
def get_favorites_view_api(request, **kwargs):
    slug = request.GET.get('slug', "")
    try:
        model = kwargs['model']
        object_model = kwargs['object_model']
        user = request.user
        my_object = object_model.objects.all().get(slug=slug)
        model.add_or_delete_favorite(user=user, obj=my_object)
        model_fav = {
            Post: user.favoritepost,
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
def get_like_or_dislike_view_api(request):
    slug = request.GET.get('slug', "")
    action = request.GET.get('action', "")
    try:
        obj = Post.objects.get(slug=slug)
        if action == 'like':
            obj.set_like_or_dislike(is_like=True)
            obj.save()
            response = JsonResponse({'status': 'Successful', 'state': 'like', 'rate': obj.rating})
            response.status_code = 200
            return response
        elif action == 'dislike':
            obj.set_like_or_dislike(is_dislike=True)
            obj.save()
            response = JsonResponse({'status': 'Successful', 'state': 'dislike', 'rate': obj.rating})
            response.status_code = 200
            return response
    except KeyError:
        response = JsonResponse({'error': 'Please specify the correct object_model'})
        response.status_code = 400
    except ObjectDoesNotExist:
        response = JsonResponse(
            {'error': f"Object with slug:{slug!r} does not exist. Please specify the correct slug"})
        response.status_code = 400
    except Exception:
        response = JsonResponse({'error': 'Unexpected error'})
        response.status_code = 400
    else:
        response = JsonResponse({'status': 'Successful', 'state': 'You already set like or dislike'})
        response.status_code = 200
        return response


@login_required
def get_comment_like_or_dislike_view_api(request):
    code_id = request.GET.get('code_id', "")
    action = request.GET.get('action', "")
    try:
        obj = Comment.objects.get(pk=code_id)
        if action == 'like':
            obj.set_like_or_dislike(is_like=True)
            obj.save()
            response = JsonResponse({'status': 'Successful', 'state': 'like', 'rate': obj.rating})
            response.status_code = 200
            return response
        elif action == 'dislike':
            obj.set_like_or_dislike(is_dislike=True)
            obj.save()
            response = JsonResponse({'status': 'Successful', 'state': 'dislike', 'rate': obj.rating})
            response.status_code = 200
            return response
    except KeyError:
        response = JsonResponse({'error': 'Please specify the correct object_model'})
        response.status_code = 400
    except ObjectDoesNotExist:
        response = JsonResponse(
            {'error': f"Object with code_id:{code_id!r} does not exist. Please specify the correct code_id"})
        response.status_code = 400
    except Exception:
        response = JsonResponse({'error': 'Unexpected error'})
        response.status_code = 400
    else:
        response = JsonResponse({'status': 'Successful', 'state': 'You already set like or dislike'})
        response.status_code = 200
        return response
