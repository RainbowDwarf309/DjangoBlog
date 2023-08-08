from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from .models import Comment, UserProfile, Post, FavoritePost, change_comment_rating_minus, change_post_rating_plus, \
    change_post_rating_minus, change_comment_rating_plus
from . import karma
from services.redis_functions import redis_set_new_posts


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.userprofile.save()


@receiver(post_save, sender=Post)
def update_karma_create_delete_post(sender, instance, created, **kwargs):
    """Add karma on creating/deleting(status) post"""
    if created:
        karma.submit_post(instance)
    elif instance.status == Post.AttrStatus.DELETED:
        karma.delete_post(instance)


@receiver(post_save, sender=Comment)
def update_karma_create_delete_comment(sender, instance, created, **kwargs):
    if created:
        karma.submit_comment(instance)
    elif instance.status == Comment.AttrStatus.DELETED:
        karma.delete_comment(instance)


@receiver(post_save, sender=FavoritePost)
def karma_add_coupon_to_favourite(sender, instance, created, **kwargs):
    if created:
        karma.add_post_to_favourite(instance.obj)


@receiver(pre_delete, sender=FavoritePost)
def karma_remove_coupon_from_favourite(sender, instance, **kwargs):
    karma.remove_post_from_favourite(instance.obj)


@receiver(change_post_rating_plus, sender=Post)
def post_plus_rating(instance, **kwargs):
    karma.post_rating_plus(instance)


@receiver(change_post_rating_minus, sender=Post)
def post_minus_rating(instance, **kwargs):
    karma.post_rating_minus(instance)


@receiver(change_comment_rating_plus, sender=Comment)
def comment_plus_rating(instance, **kwargs):
    karma.comment_rating_plus(instance)


@receiver(change_comment_rating_minus, sender=Comment)
def comment_minus_rating(instance, **kwargs):
    karma.comment_rating_minus(instance)


@receiver(post_save, sender=Post)
def create_profile(sender, instance, created, **kwargs):
    if created:
        redis_set_new_posts(instance)
