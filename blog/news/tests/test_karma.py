import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from news.karma import KarmaActionCost
from news.models import Post, ActionTrack, Comment, FavoritePost, Category


class PostKarmaTest(TestCase):
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
        self.user_credentials2 = {
            'username': 'testuser2',
            'password': 'password',
            'email': 'test@gmail.com'
        }
        self.user = User.objects.create(**self.user_credentials)
        self.user1 = User.objects.create(**self.user_credentials1)
        self.user2 = User.objects.create(**self.user_credentials2)
        self.category = Category.objects.create(title='Test')
        self.post_credentials = {
            'author': self.user,
            'title': 'Test title',
            'content': 'Test content',
            'category': self.category,
        }
        self.post_credentials1 = {
            'author': self.user,
            'title': 'Test title 1',
            'content': 'Test content',
            'category': self.category,
        }
        self.post = Post.objects.create(**self.post_credentials)
        self.post.save()

        ActionTrack.objects.create(
            user=self.user,
            action=ActionTrack.AttrAction.EVERYDAY_KARMA_GIVEN,
            page=ActionTrack.AttrPage.KARMA,
        )
        self.user.userprofile.karma = 0
        self.user.userprofile.save()

    def test_karma_on_post_creation_deleting(self):
        create_expected_value = KarmaActionCost.SUBMIT_POST.value
        created_post = Post.objects.create(**self.post_credentials1)
        created_post.save()
        self.assertEqual(self.user.userprofile.karma, create_expected_value)
        created_post.status = Post.AttrStatus.DELETED
        created_post.save()
        self.assertEqual(self.user.userprofile.karma, -int(KarmaActionCost.POST_WAS_DELETED.value))

    def test_add_to_favourite(self):
        FavoritePost.add_or_delete_favorite(user=self.user2, obj=self.post)
        self.user.userprofile.refresh_from_db()
        self.assertEqual(self.user.userprofile.karma, KarmaActionCost.ADD_POST_TO_FAVOURITE.value)

    def test_delete_from_favourite(self):
        FavoritePost.add_or_delete_favorite(user=self.user2, obj=self.post)
        FavoritePost.add_or_delete_favorite(user=self.user2, obj=self.post)
        self.user1.userprofile.refresh_from_db()
        self.assertEqual(self.user.userprofile.karma, 0)

    def test_plus_utility(self):
        self.post.set_like_or_dislike(is_like=True)
        self.user.userprofile.refresh_from_db()
        self.assertEqual(self.user.userprofile.karma, KarmaActionCost.POST_RATING_COST.value)

    def test_minus_utility(self):
        self.post.set_like_or_dislike(is_dislike=True)
        self.user.userprofile.refresh_from_db()
        self.assertEqual(self.user.userprofile.karma, -KarmaActionCost.POST_RATING_COST.value)


class CommentKarmaTest(TestCase):
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
        self.user.userprofile.karma = 0
        self.user.userprofile.save()
        self.comment_test = Comment.objects.create(
            user_submitter=self.user,
            post=self.post,
            text='new comm',
            status=Comment.AttrStatus.VISIBLE,
            parent=None,
        )
        self.comment_test.save()
        self.user.userprofile.karma = 0
        self.user.userprofile.save()

    def test_create_delete_comment(self):
        self.comment = Comment.objects.create(
            user_submitter=self.user,
            post=self.post,
            text='new comm',
            status=Comment.AttrStatus.VISIBLE,
            parent=None,
        )
        self.comment.save()
        self.user.userprofile.refresh_from_db()
        self.assertEqual(self.user.userprofile.karma, KarmaActionCost.SUBMIT_COMMENT.value)
        self.comment.status = Comment.AttrStatus.DELETED
        self.comment.save()
        self.assertEqual(self.user.userprofile.karma, -int(KarmaActionCost.COMMENT_WAS_DELETED.value))

    def test_plus_rating(self):
        self.comment_test.set_like_or_dislike(is_like=True)
        # self.comment_test.save()
        self.user.userprofile.refresh_from_db()
        self.assertEqual(self.user.userprofile.karma, KarmaActionCost.COMMENT_RATING_COST.value)

    def test_minus_rating(self):
        self.comment_test.set_like_or_dislike(is_dislike=True)
        self.user.userprofile.refresh_from_db()
        self.assertEqual(self.user.userprofile.karma, -int(KarmaActionCost.COMMENT_RATING_COST.value))
