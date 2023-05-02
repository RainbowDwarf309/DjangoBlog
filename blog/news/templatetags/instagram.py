from django import template
from news.models import Post
from datetime import datetime, timedelta

register = template.Library()


@register.inclusion_tag('news/instagram.html')
def get_popular_posts_with_link():
    time_threshold = datetime.now() - timedelta(days=7)
    posts = Post.objects.filter(link__isnull=False, is_published=True, created_at__lt=time_threshold). \
                order_by('views', 'rating')[:6]
    return {"posts": posts}
