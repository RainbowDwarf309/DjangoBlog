from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, verbose_name='Url', unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={"slug": self.slug})

    class Meta:
        verbose_name = 'Категория(ю)'
        verbose_name_plural = 'Категории'
        ordering = ['title']


class Tag(models.Model):
    title = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, verbose_name='Url', unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tag', kwargs={"slug": self.slug})

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['title']


class Post(models.Model):

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
    likes = models.PositiveBigIntegerField(default=0)
    dislikes = models.PositiveBigIntegerField(default=0)

    def get_absolute_url(self):
        return reverse('post', kwargs={"slug": self.slug})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at']
