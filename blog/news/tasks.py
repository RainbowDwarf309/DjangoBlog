from django.conf import settings
from news.models import Post
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from services.functions import get_active_newsletter_subscribers, get_popular_posts_of_day, get_popular_posts_of_week
from services.redis_functions import redis_set_popular_posts_of_day, redis_set_popular_posts_of_week
from blog.celery import app


@app.task
def set_posts_of_day_task() -> None:
    time_threshold = datetime.now() - timedelta(days=0)
    posts = Post.objects.filter(is_published=True, created_at__lt=time_threshold).order_by('views', 'likes')[:10]
    for post in posts:
        redis_set_popular_posts_of_day(post)


@app.task
def set_posts_of_week_task() -> None:
    time_threshold = datetime.now() - timedelta(days=7)
    posts = Post.objects.filter(is_published=True, created_at__lt=time_threshold).order_by('views', 'likes')[:10]
    for post in posts:
        redis_set_popular_posts_of_week(post)


@app.task
def send_posts_of_day_task() -> bool:
    subscribers = get_active_newsletter_subscribers()
    subject = 'Popular posts of the day'
    posts = get_popular_posts_of_day()
    html_message = render_to_string('news/posts_of_day.html', {
        'domain': 'http://127.0.0.1:8000',
        'posts': posts,
    })
    message = strip_tags(html_message)
    send_mail(subject, message, settings.EMAIL_HOST_USER, subscribers['Post of a day'], fail_silently=False)


@app.task
def send_posts_of_week_task() -> bool:
    subscribers = get_active_newsletter_subscribers()
    subject = 'Popular posts of the week'
    posts = get_popular_posts_of_week()
    html_message = render_to_string('news/posts_of_week.html', {
        'domain': 'http://127.0.0.1:8000',
        'posts': posts,
    })
    message = strip_tags(html_message)
    send_mail(subject, message, settings.EMAIL_HOST_USER, subscribers['Post of a week'], fail_silently=False)
