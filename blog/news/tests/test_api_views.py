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

from news.api.api_views import (
    get_favorites_view_api,
)


class GetPostViewApiTest(TestCase):
    def setUp(self) -> None:
        self.user_credentials = {
            'username': 'testuser',
            'password': 'password',
            'email': 'test@gmail.com'
        }
        self.user_credentials_2 = {
            'username': 'testuser_@',
            'password': 'password',
            'email': 'test@gmail.com'
        }

        self.user = User.objects.create(**self.user_credentials)
        self.user.save()
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

    def test_post_without_action(self):
        response = self.client.get(reverse('ajax_post'), {'code_id': self.post.pk})
        self.assertTrue(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['error'], 'Unexpected action.')

    def test_code_id_not_int(self):
        response = self.client.get(reverse('ajax_post'), {'code_id': 'test id'})
        self.assertTrue(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['error'],
                         'code_id must be integer or string of integer, and more or equal 0.')

    def test_code_id_less_zero(self):
        response = self.client.get(reverse('ajax_post'), {'code_id': -1})
        self.assertTrue(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['error'],
                         'code_id must be integer or string of integer, and more or equal 0.')

    def test_code_id_does_not_exist(self):
        code_id = 10
        response = self.client.get(reverse('ajax_post'), {'code_id': code_id})
        self.assertTrue(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['error'], f'Object with code_id={code_id} does not exist.')

    def test_post_viewed(self):
        response = self.client.get(reverse('ajax_post'), {'code_id': self.post.pk, 'action': 'viewed'})
        self.assertTrue(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['state'], 'viewed')
        self.assertEqual(json.loads(response.content)['views'], 1)
        self.assertEqual(json.loads(response.content)['rate'], 0)
        response = self.client.get(reverse('ajax_post'), {'code_id': self.post.pk, 'action': 'viewed'})
        self.assertTrue(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['state'], 'Already viewed')
        self.assertEqual(json.loads(response.content)['views'], 1)
        self.assertEqual(json.loads(response.content)['rate'], 0)

    def test_post_like(self):
        response = self.client.get(reverse('ajax_post'), {'code_id': self.post.pk, 'action': 'like'})
        self.assertTrue(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['views'], 0)
        self.assertEqual(json.loads(response.content)['rate'], 1)

    def test_post_dislike(self):
        response = self.client.get(reverse('ajax_post'), {'code_id': self.post.pk, 'action': 'dislike'})
        self.assertTrue(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['views'], 0)
        self.assertEqual(json.loads(response.content)['rate'], -1)

    def test_post_already_changed(self):
        response = self.client.get(reverse('ajax_post'), {'code_id': self.post.pk, 'action': 'dislike'})
        self.assertTrue(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['views'], 0)
        self.assertEqual(json.loads(response.content)['rate'], -1)
        response = self.client.get(reverse('ajax_post'), {'code_id': self.post.pk, 'action': 'dislike'})
        self.assertTrue(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['error'], 'Already changed.')
        self.assertEqual(json.loads(response.content)['views'], 0)
        self.assertEqual(json.loads(response.content)['rate'], -1)


class GetFavoriteViewApiTest(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.user_credentials = {
            'username': 'testuser',
            'password': 'password',
            'email': 'test@gmail.com'
        }
        self.user_credentials_2 = {
            'username': 'testuser_@',
            'password': 'password',
            'email': 'test@gmail.com'
        }

        self.user = User.objects.create(**self.user_credentials)
        self.user.save()
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

    def test_add_post_to_favorite_login_required(self):
        response = self.client.get(reverse('ajax_favorite_post'), {'slug': self.post.slug}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_add_to_favorite(self):
        self.client.force_login(user=self.user)
        response = self.client.get(reverse('ajax_favorite_post'), {'slug': self.post.slug}, follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'registration/login.html')
        self.assertEqual(json.loads(response.content)['status'], 'Successful')
        self.assertEqual(json.loads(response.content)['state'], 'added')
        self.assertEqual(FavoritePost.objects.get(pk=1).obj, self.post)

    def test_delete_from_favorite(self):
        self.client.force_login(user=self.user)
        self.client.get(reverse('ajax_favorite_post'), {'slug': self.post.slug}, follow=True)
        response = self.client.get(reverse('ajax_favorite_post'), {'slug': self.post.slug}, follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'registration/login.html')
        self.assertEqual(json.loads(response.content)['status'], 'Successful')
        self.assertEqual(json.loads(response.content)['state'], 'deleted')
        self.assertQuerysetEqual(FavoritePost.objects.all(), Post.objects.none())

    def test_add_post_to_favorite_model_unexpected_slug(self):
        self.client.force_login(user=self.user)
        response = self.client.get(reverse('ajax_favorite_post'), {'slug': 'post_slug'}, follow=True)
        self.assertEqual(response.status_code, 400)
        self.assertTemplateNotUsed(response, 'registration/login.html')
        data = response.json()
        expected_data = {'error': "Object with slug:'post_slug' does not exist. Please specify the correct slug"}
        self.assertEqual(data, expected_data)
        response = self.client.get(reverse('ajax_favorite_post'), {'slug': ''}, follow=True)
        self.assertEqual(response.status_code, 400)
        self.assertTemplateNotUsed(response, 'registration/login.html')
        data = response.json()
        expected_data = {'error': "Object with slug:'' does not exist. Please specify the correct slug"}
        self.assertEqual(data, expected_data)
        response = self.client.get(reverse('ajax_favorite_post'), {'slug': '/'}, follow=True)
        self.assertEqual(response.status_code, 400)
        self.assertTemplateNotUsed(response, 'registration/login.html')
        data = response.json()
        expected_data = {'error': "Object with slug:'/' does not exist. Please specify the correct slug"}
        self.assertEqual(data, expected_data)

    def test_add_post_to_favorite_model_no_model(self):
        self.client.force_login(user=self.user)
        test_request = self.factory.get('/ajax/favorite_post/?slug=asd1')
        test_request.user = self.user
        response = get_favorites_view_api(test_request, object_model=Post)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['error'], "Please specify the correct model and object_model")

    def test_add_post_to_favorite_model_no_object_model(self):
        self.client.force_login(user=self.user)
        test_request = self.factory.get('/ajax/favorite_post/?slug=asd1')
        test_request.user = self.user
        response = get_favorites_view_api(test_request, model=FavoritePost)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['error'], "Please specify the correct model and object_model")

    def test_add_post_to_favorite_model_kwargs_are_strings(self):
        self.client.force_login(user=self.user)
        test_request = self.factory.get(f'/ajax/favorite_post/?slug={self.post.slug}')
        test_request.user = self.user
        response = get_favorites_view_api(test_request, model='FavoritePost', object_model='Post')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['error'], "Unexpected error")


class GetPostRatingViewApiTest(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.user_credentials = {
            'username': 'testuser',
            'password': 'password',
            'email': 'test@gmail.com'
        }
        self.user_credentials_2 = {
            'username': 'testuser_@',
            'password': 'password',
            'email': 'test@gmail.com'
        }

        self.user = User.objects.create(**self.user_credentials)
        self.user.save()
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

    def test_add_post_to_favorite_login_required(self):
        response = self.client.get(reverse('ajax_post_like_dislike'), {'slug': self.post.slug, 'action': 'like'},
                                   follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_set_like_post(self):
        self.client.force_login(user=self.user)
        response = self.client.get(reverse('ajax_post_like_dislike'), {'slug': self.post.slug, 'action': 'like'},
                                   follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'registration/login.html')
        self.assertEqual(json.loads(response.content)['status'], 'Successful')
        self.assertEqual(json.loads(response.content)['state'], 'like')
        self.assertEqual(json.loads(response.content)['rate'], 1)

    def test_set_dislike_post(self):
        self.client.force_login(user=self.user)
        response = self.client.get(reverse('ajax_post_like_dislike'), {'slug': self.post.slug, 'action': 'dislike'},
                                   follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'registration/login.html')
        self.assertEqual(json.loads(response.content)['status'], 'Successful')
        self.assertEqual(json.loads(response.content)['state'], 'dislike')
        self.assertEqual(json.loads(response.content)['rate'], -1)

    def test_already_change_post_rating(self):
        self.client.force_login(user=self.user)
        self.client.get(reverse('ajax_post_like_dislike'), {'slug': self.post.slug, 'action': 'dislike'}, follow=True)
        response = self.client.get(reverse('ajax_post_like_dislike'), {'slug': self.post.slug, 'action': 'dislike'},
                                   follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'registration/login.html')
        self.assertEqual(json.loads(response.content)['error'], 'You already set like or dislike.')
        self.assertEqual(json.loads(response.content)['rate'], -1)

    def test_post_without_action(self):
        self.client.force_login(user=self.user)
        response = self.client.get(reverse('ajax_post_like_dislike'), {'slug': self.post.slug, 'action': 'dad'},
                                   follow=True)
        self.assertTrue(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['error'], 'Unexpected action.')

    def test_change_rate_with_unexpected_slug(self):
        self.client.force_login(user=self.user)
        response = self.client.get(reverse('ajax_post_like_dislike'), {'slug': 'post_slug', 'action': 'dislike'},
                                   follow=True)
        self.assertEqual(response.status_code, 400)
        self.assertTemplateNotUsed(response, 'registration/login.html')
        data = response.json()
        expected_data = {'error': "Object with slug:'post_slug' does not exist. Please specify the correct slug"}
        self.assertEqual(data, expected_data)
        response = self.client.get(reverse('ajax_post_like_dislike'), {'slug': '', 'action': 'like'}, follow=True)
        self.assertEqual(response.status_code, 400)
        self.assertTemplateNotUsed(response, 'registration/login.html')
        data = response.json()
        expected_data = {'error': "Object with slug:'' does not exist. Please specify the correct slug"}
        self.assertEqual(data, expected_data)
        response = self.client.get(reverse('ajax_post_like_dislike'), {'slug': '/', 'action': 'dislike'}, follow=True)
        self.assertEqual(response.status_code, 400)
        self.assertTemplateNotUsed(response, 'registration/login.html')
        data = response.json()
        expected_data = {'error': "Object with slug:'/' does not exist. Please specify the correct slug"}
        self.assertEqual(data, expected_data)

    def test_change_rate_om_deleted_post(self):
        self.post.status = Post.AttrStatus.DELETED
        self.post.save()
        self.client.force_login(user=self.user)
        response = self.client.get(reverse('ajax_post_like_dislike'), {'slug': self.post.slug, 'action': 'dislike'},
                                   follow=True)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['error'], 'Sorry, post deleted.')


class GetCommentRatingViewApiTest(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.user_credentials = {
            'username': 'testuser',
            'password': 'password',
            'email': 'test@gmail.com'
        }
        self.user_credentials_2 = {
            'username': 'testuser_@',
            'password': 'password',
            'email': 'test@gmail.com'
        }

        self.user = User.objects.create(**self.user_credentials)
        self.user.save()
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
        self.comment = Comment.objects.create(
            user_submitter=self.user,
            post=self.post,
            text='new comm',
            status=Comment.AttrStatus.VISIBLE,
            parent=None,
        )
        self.comment.save()

        self.comment_child = Comment.objects.create(
            user_submitter=self.user,
            post=self.post,
            text='new comm2',
            status=Comment.AttrStatus.VISIBLE,
            parent=self.comment,
        )
        self.comment_child.save()

    def test_set_like_comment(self):
        self.client.force_login(user=self.user)
        response = self.client.get(reverse('ajax_comment_like_dislike'), {'code_id': self.comment.pk, 'action': 'like'},
                                   follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'registration/login.html')
        self.assertEqual(json.loads(response.content)['status'], 'Successful')
        self.assertEqual(json.loads(response.content)['state'], 'like')
        self.assertEqual(json.loads(response.content)['rate'], 1)

    def test_set_dislike_comment(self):
        self.client.force_login(user=self.user)
        response = self.client.get(reverse('ajax_comment_like_dislike'),
                                   {'code_id': self.comment.pk, 'action': 'dislike'},
                                   follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'registration/login.html')
        self.assertEqual(json.loads(response.content)['status'], 'Successful')
        self.assertEqual(json.loads(response.content)['state'], 'dislike')
        self.assertEqual(json.loads(response.content)['rate'], -1)

    def test_already_change_comment_rating(self):
        self.client.force_login(user=self.user)
        self.client.get(reverse('ajax_comment_like_dislike'), {'code_id': self.comment.pk, 'action': 'dislike'},
                        follow=True)
        response = self.client.get(reverse('ajax_comment_like_dislike'),
                                   {'code_id': self.comment.pk, 'action': 'dislike'}, follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'registration/login.html')
        self.assertEqual(json.loads(response.content)['error'], 'You already set like or dislike.')
        self.assertEqual(json.loads(response.content)['rate'], -1)

    def test_comment_without_action(self):
        self.client.force_login(user=self.user)
        response = self.client.get(reverse('ajax_comment_like_dislike'), {'code_id': self.comment.pk, 'action': 'dad'},
                                   follow=True)
        self.assertTrue(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['error'], 'Unexpected action.')

    def test_change_rate_with_unexpected_id(self):
        self.client.force_login(user=self.user)
        response = self.client.get(reverse('ajax_comment_like_dislike'), {'code_id': '341', 'action': 'dislike'},
                                   follow=True)
        self.assertEqual(response.status_code, 400)
        self.assertTemplateNotUsed(response, 'registration/login.html')
        data = response.json()
        expected_data = {'error': "Object with code_id:'341' does not exist. Please specify the correct code_id"}
        self.assertEqual(data, expected_data)
        response = self.client.get(reverse('ajax_comment_like_dislike'), {'code_id': '-20', 'action': 'dislike'},
                                   follow=True)
        self.assertEqual(response.status_code, 400)
        self.assertTemplateNotUsed(response, 'registration/login.html')
        data = response.json()
        expected_data = {'error': "Unexpected error"}
        self.assertEqual(data, expected_data)
        response = self.client.get(reverse('ajax_comment_like_dislike'), {'code_id': '', 'action': 'like'}, follow=True)
        self.assertEqual(response.status_code, 400)
        self.assertTemplateNotUsed(response, 'registration/login.html')
        data = response.json()
        expected_data = {'error': "Unexpected error"}
        self.assertEqual(data, expected_data)
        response = self.client.get(reverse('ajax_comment_like_dislike'), {'code_id': '/', 'action': 'dislike'},
                                   follow=True)
        self.assertEqual(response.status_code, 400)
        self.assertTemplateNotUsed(response, 'registration/login.html')
        data = response.json()
        expected_data = {'error': "Unexpected error"}
        self.assertEqual(data, expected_data)

    def test_change_rate_om_deleted_comment(self):
        self.comment.status = Comment.AttrStatus.DELETED
        self.comment.save()
        self.client.force_login(user=self.user)
        response = self.client.get(reverse('ajax_comment_like_dislike'), {'code_id': self.comment.pk,
                                                                          'action': 'dislike'},
                                   follow=True)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['error'], 'Sorry, comment deleted.')

    def test_change_rate_om_invisible_comment(self):
        self.comment.status = Comment.AttrStatus.INVISIBLE
        self.comment.save()
        self.client.force_login(user=self.user)
        response = self.client.get(reverse('ajax_comment_like_dislike'), {'code_id': self.comment.pk,
                                                                          'action': 'dislike'},
                                   follow=True)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['error'], 'Sorry, comment invalid.')
