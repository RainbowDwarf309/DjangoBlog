from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.urls import reverse
import json

from news.models import (
    Post,
    Category,
    Comment,
    FavoritePost
)

from services.functions import (
    get_client_ip,
    get_param_from_request,
    track_action,
    get_session_key,
    get_post_from_slug
)


class GetClientIP(TestCase):
    def setUp(self) -> None:
        self.request = self.client.get(reverse('home')).wsgi_request

    def test_(self):
        self.assertEqual(get_client_ip(self.request), '127.0.0.1')

    def test_x_forwarded_for(self):
        x_forwarded_for = get_param_from_request(self.request, 'HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            self.assertEqual(x_forwarded_for.split(',')[0], '127.0.0.1')

    def test_remote_addr(self):
        self.assertEqual(self.request.META.get('REMOTE_ADDR'), '127.0.0.1')


class GetParamFromRequest(TestCase):
    def setUp(self) -> None:
        self.request = self.client.get(reverse('home')).wsgi_request

    def test_(self):
        self.assertEqual(get_param_from_request(self.request, 'HTTP_REFERER'), self.request.META.get('HTTP_REFERER'))

    def test_none(self):
        self.assertIsNone(get_param_from_request(self.request, 'asdasd'))


class GetSessionKey(TestCase):
    def setUp(self) -> None:
        self.request = self.client.get(reverse('home')).wsgi_request

    def test_(self):
        self.assertEqual(get_session_key(self.request), self.request.session.session_key)


class MyTestClass:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class GetCouponFromSlugTest(TestCase):
    def setUp(self) -> None:
        self.user_credentials = {
            'username': 'testuser',
            'password': 'password'}
        self.user = User.objects.create_user(**self.user_credentials)

        self.category = Category.objects.create(title='Test')
        self.category.save()
        self.post_credentials = {
            'author': self.user,
            'title': 'Test title',
            'content': 'Test content',
            'category': self.category,
        }
        self.post = Post.objects.create(**self.post_credentials)
        self.post.save()

    def test_not_exist(self):
        my_class = MyTestClass(kwargs={'slug': 'someslug'})
        self.assertFalse(get_post_from_slug(my_class))  # Obj doesn't exist

    def test_exist(self):
        my_class = MyTestClass(kwargs={'slug': self.post.slug})
        self.assertEqual(get_post_from_slug(my_class), self.post)

    def test_not_slug(self):
        my_class = MyTestClass(kwargs={'another-slug': self.post.slug})
        self.assertEqual(get_post_from_slug(my_class, slug='another-slug'), self.post)
