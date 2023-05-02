from django import template
from news.models import Post
from datetime import datetime, timedelta

register = template.Library()


@register.inclusion_tag('news/featured_posts.html')
def get_featured_posts():
    time_threshold = datetime.now() - timedelta(days=1)
    posts = Post.objects.filter(category__title__in=['IT Technology', 'Politic', 'Sport', 'Science', 'Adventure'],
                                is_published=True,
                                created_at__lt=time_threshold).order_by('views', 'rating')[:4]
    return {"posts": posts}
