from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify
from PIL import Image
from mptt.models import MPTTModel, TreeForeignKey


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('User'))
    avatar = models.ImageField(upload_to='photos/avatars/%Y/%m/%d/', verbose_name='User avatar', blank=False,
                               default='photos/default_user_avatar.png',
                               help_text=_('Only .png format. Less than 0.5mb.'))
    bio = models.TextField(blank=True, max_length=200, verbose_name=_('information'))
    first_name = models.CharField(max_length=60, blank=True, null=True)
    last_name = models.CharField(max_length=60, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    karma = models.BigIntegerField(verbose_name="Total karma", default=0)

    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.avatar.path)
        # resize image
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.avatar.path)


class Category(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, verbose_name='Url', unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={"slug": self.slug})

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['title']

    def save(self, *args, **kwargs):
        created = not self.pk
        super().save(*args, **kwargs)
        if created:
            Tag.objects.create(title=str(self.title).lower(), slug=self.slug)


class Tag(models.Model):
    title = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, verbose_name='Url', unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tag', kwargs={"slug": self.slug})

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ['title']


class Post(models.Model):
    class AttrStatus(models.TextChoices):
        APPROVED = 'APPROVED'
        DELETED = 'DELETED'

    title = models.CharField(max_length=150, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, verbose_name='Url', unique=True)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='автор поста')
    content = models.TextField(blank=True, verbose_name='Содержание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Фото', blank=True)
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория')
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    views = models.IntegerField(default=0)
    status = models.CharField(max_length=15, choices=AttrStatus.choices,
                              default=AttrStatus.APPROVED,
                              verbose_name=_('Status'))
    likes = models.PositiveBigIntegerField(default=0)
    dislikes = models.PositiveBigIntegerField(default=0)
    rating = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('post', kwargs={"slug": self.slug})

    def __str__(self):
        return f"{self.title}, {self.author}, {self.category}, {self.slug}, {self.tags}"

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def set_like_or_dislike(self, is_like: bool = False, is_dislike: bool = False) -> None:
        if is_like:
            self.likes += 1
            self.rating += 1
        elif is_dislike:
            self.dislikes += 1
            self.rating -= 1
        self.save()

class Comment(MPTTModel):
    class AttrStatus(models.TextChoices):
        VISIBLE = 'VISIBLE'
        INVISIBLE = 'INVISIBLE'
        DELETED = 'DELETED'

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user_submitter = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='comment_user_submitter',
                                       verbose_name=_('User submitter'))
    text = models.TextField(max_length=250, verbose_name=_('Comment text'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Date of creation'))
    parent = TreeForeignKey('self', blank=True, null=True, on_delete=models.CASCADE,
                            verbose_name='Parent comment', related_name='child')
    status = models.CharField(max_length=15, choices=AttrStatus.choices,
                              default=AttrStatus.VISIBLE,
                              verbose_name='Status')
    rating = models.IntegerField(default=0, verbose_name=_('Rating'))
    count_of_likes = models.PositiveIntegerField(default=0, verbose_name='Count of likes')
    count_of_dislikes = models.PositiveIntegerField(default=0, verbose_name='Count of dislikes')

    class MPTTMeta:
        order_insertion_by = ['created_at']

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
        ordering = ['created_at']

    def __str__(self):
        return self.text

    def set_like_or_dislike(self, is_like: bool = False, is_dislike: bool = False) -> None:
        if is_like:
            self.count_of_likes += 1
            self.rating += 1
        elif is_dislike:
            self.count_of_dislikes += 1
            self.rating -= 1
        self.save()


class Favorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s',
                             verbose_name=_('User'))

    class Meta:
        abstract = True

    @classmethod
    def add_or_delete_favorite(cls, user, obj):
        raise NotImplementedError('You must specify add_or_delete_favorite method')


class FavoritePost(Favorites):
    obj = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name=_('Post'))

    def __str__(self):
        return f'User:{self.user}, Favorite Post:{self.obj}'

    @classmethod
    def add_or_delete_favorite(cls, user, obj):
        favorite, created = cls.objects.get_or_create(user=user, obj_id=obj.pk)
        if not created:
            favorite.delete()
