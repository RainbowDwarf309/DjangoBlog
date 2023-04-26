from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


TEST_DIR = 'test_data'

from news.models import (
    Post,
    Category,
    Comment,
    Tag,
)

from news.views import (
    HomeView,
    SinglePostView,
    PostsByCategoryView,
    PostsByTagView,
    CreatePostView,
)


class HomeViewTest(TestCase):

    def test_context(self):
        response = self.client.get(reverse('home'))
        self.assertQuerysetEqual(response.context['posts'], Post.objects.filter(is_published=True, status='APPROVED'))
        self.assertQuerysetEqual(response.context['title'], 'Django Blog')

    def test_template_name(self):
        self.assertEqual(HomeView.template_name, 'news/index.html')

    def test_context_object_name(self):
        self.assertEqual(HomeView.context_object_name, 'posts')


class SinglePostViewTest(TestCase):

    def setUp(self) -> None:
        self.user_credentials = {
            'username': 'testuser',
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
            'photo': 'logo.jpeg'
        }
        self.post = Post.objects.create(**self.post_credentials)
        self.post.save()



    def test_context(self):
        self.client.force_login(user=self.user)
        response = self.client.get(reverse('post', kwargs={'slug': self.post.slug}))
        self.assertEquals(response.context['is_favorite'], self.user.favoritepost.filter(
            obj=self.post).exists()),
        self.assertEquals(response.context['comments_count'],
                          Comment.objects.filter(post=Post.objects.select_related('author__userprofile').
                                                 get(slug=self.post.slug)).count()
                          )
        self.assertQuerysetEqual(response.context['comments'],
                                 Comment.objects.exclude(status=Comment.AttrStatus.INVISIBLE). \
                                 select_related('post', 'user_submitter__userprofile', 'parent'). \
                                 filter(post=Post.objects.select_related('author__userprofile'). \
                                        get(slug=self.post.slug)))

    def test_context_comments(self):
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
        response = self.client.get(reverse('post', kwargs={'slug': self.post.slug}))
        self.assertQuerysetEqual(response.context['comments'],
                                 self.post.comments.exclude(status=Comment.AttrStatus.INVISIBLE))

        self.assertEqual(response.context['comments'].count(), 2)

    def test_context_comments_invisible(self):
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
            status=Comment.AttrStatus.INVISIBLE,
            parent=self.comment,
        )
        self.comment_child.save()
        response = self.client.get(reverse('post', kwargs={'slug': self.post.slug}))
        self.assertNotIn(self.comment_child, response.context['comments'])

    def test_template_name(self):
        self.assertEqual(SinglePostView.template_name, 'news/single_post.html')

    def test_context_object_name(self):
        self.assertEqual(SinglePostView.context_object_name, 'post')


class PostsByCategoryViewTest(TestCase):

    def setUp(self) -> None:
        self.user_credentials = {
            'username': 'testuser',
            'password': 'password',
            'email': 'test@gmail.com'
        }
        # script_location = Path(__file__).absolute().parent
        #
        # self.test_image_path_png = script_location / 'logo-company.png'

        self.user = User.objects.create(**self.user_credentials)
        self.user.save()
        self.category = Category.objects.create(title='Test')
        self.category.save()
        self.post_credentials = {
            'author': self.user,
            'title': 'Test title',
            'content': 'Test content',
            'category': self.category,
            'photo': 'logo.jpeg'
        }
        self.post = Post.objects.create(**self.post_credentials)
        self.post.save()

    def test_context(self):
        response = self.client.get(reverse('category', kwargs={'slug': self.category.slug}))
        self.assertQuerysetEqual(response.context['posts'],
                                 Post.objects.filter(category=Category.objects.get(slug=self.category.slug),
                                                     is_published=True))
        self.assertEquals(response.context['title'], Category.objects.get(slug=self.category.slug))

    def test_template_name(self):
        self.assertEqual(PostsByCategoryView.template_name, 'news/index.html')

    def test_context_object_name(self):
        self.assertEqual(PostsByCategoryView.context_object_name, 'posts')


class PostsByTagViewTest(TestCase):

    def setUp(self) -> None:
        self.user_credentials = {
            'username': 'testuser',
            'password': 'password',
            'email': 'test@gmail.com'
        }
        # script_location = Path(__file__).absolute().parent
        #
        # self.test_image_path_png = script_location / 'logo-company.png'

        self.user = User.objects.create(**self.user_credentials)
        self.user.save()
        self.category = Category.objects.create(title='Test')
        self.category.save()
        self.tag = Tag.objects.get(title='test')
        self.tag.save()
        self.post_credentials = {
            'author': self.user,
            'title': 'Test title',
            'content': 'Test content',
            'category': self.category,
            'photo': 'logo.jpeg'
        }
        self.post = Post.objects.create(**self.post_credentials)
        self.post.tags.set(Tag.objects.filter(title='test'))
        self.post.save()

    def test_context(self):
        response = self.client.get(reverse('tag', kwargs={'slug': self.tag.slug}))
        self.assertQuerysetEqual(response.context['posts'],
                                 Post.objects.filter(tags=Tag.objects.get(slug=self.tag.slug),
                                                     is_published=True))
        self.assertEquals(response.context['title'], Tag.objects.get(slug=self.tag.slug))

    def test_template_name(self):
        self.assertEqual(PostsByTagView.template_name, 'news/index.html')

    def test_context_object_name(self):
        self.assertEqual(PostsByTagView.context_object_name, 'posts')


class CreatePostViewTest(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(username='testuser', password='password', email='test@gmail.com')
        self.client.force_login(user=self.user)

    def test_template_name(self):
        self.assertEqual(CreatePostView.template_name, 'news/create_post.html')
        response = self.client.get(reverse('create_post'))
        self.assertTemplateUsed(response, "news/create_post.html")
