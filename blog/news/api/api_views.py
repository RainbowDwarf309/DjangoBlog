# from coupon_site import utils
from news.models import Post
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie




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
