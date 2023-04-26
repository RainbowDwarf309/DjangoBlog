from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from news.models import (
    Post,
    Category,
    Comment,
    Tag,
    FavoritePost
)


class PostTest(TestCase):
    def setUp(self) -> None:
        self.user_credentials = {
            'username': 'testuser',
            'password': 'password',
            'email': 'test@gmail.com'
        }
        self.user = User.objects.create(**self.user_credentials)
        self.category = Category.objects.create(title='Test')
        self.post_credentials = {
            'author': self.user,
            'title': 'Test title',
            'content': 'Test content',
            'category': self.category,
        }
        self.post = Post.objects.create(**self.post_credentials)
        self.post.save()

    def test_post_slug_autofill(self):
        self.assertIsNotNone(self.post.slug)

    def test_post_slug_correct(self):
        self.assertEquals(self.post.slug, 'test-title')

    def test_get_post_status_approved(self):
        self.assertEquals(self.post.status, 'APPROVED')

    def test_get_post_status_deleted(self):
        self.post.status = Post.AttrStatus.DELETED
        self.assertEquals(self.post.status, 'DELETED')

    def test_set_like_post(self):
        self.post.set_like_or_dislike(is_like=True)
        self.post.save()
        self.assertEquals(self.post.rating, 1)

    def test_set_dislike_post(self):
        self.post.set_like_or_dislike(is_dislike=True)
        self.post.save()
        self.assertEquals(self.post.rating, -1)

    def test_get_post_author_name(self):
        self.assertEquals(self.post.author.username, 'testuser')

    def test_get_post_category(self):
        self.assertEquals(self.post.category.title, 'Test')

    def test_absolute_url(self):
        self.assertEquals(reverse('post', kwargs={"slug": self.post.slug}), self.post.get_absolute_url())


class CategoryTest(TestCase):

    def setUp(self) -> None:
        self.category = Category.objects.create(title='Test category')
        self.category.save()

    def test_category_slug_autofill(self):
        self.assertIsNotNone(self.category.slug)

    def test_category_slug_correct(self):
        self.assertEquals(self.category.slug, 'test-category')

    def test_tag_creation(self):
        self.tag = Tag.objects.get(title=str(self.category.title).lower())
        self.assertEquals(self.tag.title, 'test category')
        self.assertIsNotNone(self.tag.slug)
        self.assertEquals(self.tag.slug, 'test-category')

    def test_absolute_url(self):
        self.assertEquals(reverse('category', kwargs={"slug": 'test-category'}), self.category.get_absolute_url())


class TagTest(TestCase):

    def setUp(self) -> None:
        self.tag = Tag.objects.create(title='Test Tag')
        self.tag.save()

    def test_tag_slug_autofill(self):
        self.assertIsNotNone(self.tag.slug)

    def test_tag_slug_correct(self):
        self.assertEquals(self.tag.slug, 'test-tag')

    def test_tag_title_lower_case(self):
        self.assertNotEquals(self.tag.title, 'Test Tag')
        self.assertEquals(self.tag.title, 'test tag')

    def test_absolute_url(self):
        self.assertEquals(reverse('tag', kwargs={"slug": self.tag.slug}), self.tag.get_absolute_url())


class CommentTest(TestCase):
    def setUp(self) -> None:
        self.user_credentials = {
            'username': 'testuser',
            'password': 'password',
            'email': 'some@mailcom',
        }
        self.user = User.objects.create_user(**self.user_credentials)
        self.category = Category.objects.create(title='Test')
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

    def test_create_comment(self):
        self.assertEquals(self.comment_child.parent, self.comment)

    def test_comment_hide(self):
        self.comment.status = Comment.AttrStatus.INVISIBLE
        self.comment.save()
        self.assertEquals(self.comment.status, Comment.AttrStatus.INVISIBLE)
        self.assertEquals(self.comment_child.status, Comment.AttrStatus.VISIBLE)

    def test_first_node(self):
        self.new_comment = Comment.objects.create(
            user_submitter=self.user,
            post=self.post,
            text='new comm',
            status=Comment.AttrStatus.VISIBLE,
            parent=None,
        )
        self.new_comment.save()
        self.assertEquals(self.new_comment.status, Comment.AttrStatus.VISIBLE)

    def test_delete_visible_comment(self):
        self.assertEqual(self.comment.status, Comment.AttrStatus.VISIBLE)
        self.comment.delete_comment()
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.status, Comment.AttrStatus.DELETED)

    def test_hide_visible_comment(self):
        self.assertEqual(self.comment.status, Comment.AttrStatus.VISIBLE)
        self.comment.hide_comment()
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.status, Comment.AttrStatus.INVISIBLE)

    def test_set_like_comment(self):
        self.comment.set_like_or_dislike(is_like=True)
        self.comment.save()
        self.assertEquals(self.comment.rating, 1)

    def test_set_dislike_comment(self):
        self.comment.set_like_or_dislike(is_dislike=True)
        self.comment.save()
        self.assertEquals(self.comment.rating, -1)


class FavoriteCouponTest(TestCase):
    def setUp(self) -> None:
        self.user1_credentials = {
            'username': 'testuser1',
            'password': 'password',
            'email': 'some@mailcom',
        }
        self.user1 = User.objects.create_user(**self.user1_credentials)
        self.user2_credentials = {
            'username': 'testuser2',
            'password': 'password',
            'email': 'some@mailcom',
        }
        self.user2 = User.objects.create_user(**self.user2_credentials)
        self.category = Category.objects.create(title='Test category')
        self.category.save()

        self.post1_credentials = {
            'author': self.user1,
            'title': 'Test post1',
            'content': 'Test content',
            'category': self.category,
        }
        self.post1 = Post.objects.create(**self.post1_credentials)
        self.post1.save()

        self.post2_credentials = {
            'author': self.user1,
            'title': 'Test post2',
            'content': 'Test content',
            'category': self.category,
        }
        self.post2 = Post.objects.create(**self.post2_credentials)
        self.post2.save()

    def test_add_post_to_favorite_model(self):
        FavoritePost.add_or_delete_favorite(user=self.user1, obj=self.post1)
        self.assertEqual(FavoritePost.objects.get(obj__pk=self.post1.pk).obj, self.post1)

    def test_delete_post_from_favorite_model(self):
        FavoritePost.add_or_delete_favorite(user=self.user1, obj=self.post1)
        FavoritePost.add_or_delete_favorite(user=self.user1, obj=self.post1)
        self.assertQuerysetEqual(FavoritePost.objects.all(), Post.objects.none())

    def test_multiple_users_add_post_to_favorite_model(self):
        FavoritePost.add_or_delete_favorite(user=self.user1, obj=self.post1)
        self.assertEqual(
            FavoritePost.objects.get(obj__pk=self.post1.pk, user=self.user1).obj,
            self.post1,
        )
        FavoritePost.add_or_delete_favorite(user=self.user2, obj=self.post1)
        self.assertEqual(
            FavoritePost.objects.get(obj__pk=self.post1.pk, user=self.user2).obj,
            self.post1)
        self.assertEqual(
            self.user1.favoritepost.get(user__pk=self.user1.pk, obj__pk=self.post1.pk),
            FavoritePost.objects.get(user__pk=self.user1.pk, obj__pk=self.post1.pk)
        )
        self.assertEqual(
            self.user2.favoritepost.get(user__pk=self.user2.pk, obj__pk=self.post1.pk),
            FavoritePost.objects.get(user__pk=self.user2.pk, obj__pk=self.post1.pk)
        )
        FavoritePost.add_or_delete_favorite(user=self.user2, obj=self.post1)
        self.assertQuerysetEqual(self.user2.favoritepost.all(), Post.objects.none())


