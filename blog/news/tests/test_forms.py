from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.urls import reverse
import json
from django.core.files.uploadedfile import SimpleUploadedFile
from pathlib import Path

from news.models import (
    Post,
    Category,
    Comment,
    FavoritePost,
    Newsletter,
    NewsType
)

from news.forms import (
    UserProfileUpdateForm,
    CreatePostForm,
    CommentSubmitForm,
    EmailChangeForm,
    NewsletterForm,
)


class UserProfileUpdateFormTest(TestCase):

    def setUp(self) -> None:
        self.user_credentials = {
            'username': 'testuser',
            'password': 'password'}
        self.user = User.objects.create_user(**self.user_credentials)
        self.user.refresh_from_db()
        script_location = Path(__file__).absolute().parent
        self.test_image_path = script_location / 'default_user_avatar.png'
        self.test_image_path_jpg = script_location / 'logo_company.jpg'
        self.test_image_path_large = script_location / 'logo_company_large.png'

    def test_clean_avatar_valid(self):
        post_dict = {
            'first_name': 'first',
            'last_name': 'Last',
            'bio': 'hey https://testlink.com/',
        }
        with open(self.test_image_path, 'rb') as f:
            form = UserProfileUpdateForm(data=post_dict,
                                         files={'avatar': SimpleUploadedFile('avatar.png', f.read())})
            self.assertTrue(form.is_valid())

    def test_clean_blank_avatar(self):
        post_dict = {
            'first_name': 'first',
            'last_name': 'Last',
            'bio': 'hey https://testlink.com/',
        }
        with open(self.test_image_path, 'rb'):
            form = UserProfileUpdateForm(data=post_dict, files={'avatar': ''})
            self.assertFalse(form.is_valid())
            self.assertEqual("Couldn't read image. Please, update avatar.", form.errors['avatar'][0])

    def test_clean_avatar_without_field(self):
        post_dict = {
            'first_name': 'first',
            'last_name': 'Last',
            'bio': 'hey https://testlink.com/',
        }
        form = UserProfileUpdateForm(data=post_dict)
        self.assertFalse(form.is_valid())
        self.assertEqual("Couldn't read image. Please, update avatar.", form.errors['avatar'][0])

    def test_clean_avatar_none(self):
        post_dict = {
            'first_name': 'first',
            'last_name': 'Last',
            'bio': 'hey https://testlink.com/',
        }
        form = UserProfileUpdateForm(data=post_dict, files={'avatar': None})
        self.assertFalse(form.is_valid())
        self.assertEqual("Couldn't read image. Please, update avatar.", form.errors['avatar'][0])

    def test_clean_avatar_not_png(self):
        post_dict = {
            'first_name': 'first',
            'last_name': 'Last',
            'bio': 'hey https://testlink.com/',
        }
        with open(self.test_image_path_jpg, 'rb') as f:
            form = UserProfileUpdateForm(data=post_dict, files={'avatar': SimpleUploadedFile('avatar.jpg', f.read())})
            self.assertFalse(form.is_valid())
            self.assertEqual(form.errors['avatar'][0], "Image must be in .png format")

    def test_clean_avatar_size(self):
        post_dict = {
            'first_name': 'first',
            'last_name': 'Last',
            'bio': 'hey https://testlink.com/',
        }

        with open(self.test_image_path_large, 'rb') as f:
            form = UserProfileUpdateForm(data=post_dict, files={'avatar': SimpleUploadedFile('avatar.jpg', f.read())})
            self.assertFalse(form.is_valid())
            self.assertEqual(form.errors['avatar'][0], "Image file too large ( > 0.5 mb )")


class SubmitPostTest(TestCase):
    def setUp(self) -> None:
        self.user_credentials = {
            'username': 'testuser',
            'password': 'password'}
        self.user = User.objects.create_user(**self.user_credentials)
        self.category = Category.objects.create(title='Test')
        self.category.save()

    def test_valid(self):
        post_dict = {
            'title': 'SomeTitle',
            'author': self.user,
            'category': self.category,
            'content': 'test content'
        }
        form = CreatePostForm(data=post_dict)
        self.assertTrue(form.is_valid())
        form.save()
        post = Post.objects.get(title='SomeTitle')
        self.assertIsNotNone(post)

    def test_valid_title_starts_with_number(self):
        post_dict = {
            'title': '3SomeTitle',
            'author': self.user,
            'category': self.category,
            'content': 'test content'
        }
        form = CreatePostForm(data=post_dict)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['title'][0], 'The title must not begin with a number')


class NewsletterFormTest(TestCase):
    def setUp(self) -> None:
        self.user_credentials = {
            'username': 'testuser',
            'password': 'password',
            'email': 'test@gmail.com'
        }
        self.user_credentials1 = {
            'username': 'testuser1',
            'password': 'password',
            'email': 'test@gmail.com'
        }
        self.user = User.objects.create_user(**self.user_credentials)
        self.user1 = User.objects.create_user(**self.user_credentials1)
        self.notification = NewsType.objects.create(type_of_news='notification')

    def test_valid(self):
        form_credentials = {
            'user': self.user,
            'email': self.user.email,
        }
        form = NewsletterForm(data=form_credentials)
        self.assertTrue(form.is_valid())

    def test_object_created(self):
        form_credentials = {
            'user': self.user,
            'email': self.user.email,
        }
        form = NewsletterForm(data=form_credentials)
        self.assertTrue(form.is_valid())
        form.save()
        newsletter = Newsletter.objects.get(user=self.user)
        self.assertIsNotNone(newsletter)

    def test_email_already_exist(self):
        form_credentials = {
            'user': self.user,
            'email': self.user.email,
        }
        form_credentials1 = {
            'user': self.user1,
            'email': self.user1.email,
        }
        form = NewsletterForm(data=form_credentials)
        form.save()
        form = NewsletterForm(data=form_credentials1)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'][0], 'User with this email already exists')
