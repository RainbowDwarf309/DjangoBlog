from django import template
from news.models import Post, Tag

register = template.Library()


@register.inclusion_tag('news/tags.html')
def get_tags():
    tags = Tag.objects.all()[:30]
    return {"tags": tags}


@register.inclusion_tag('news/popular_posts.html')
def get_popular_posts():
    posts = Post.objects.select_related('category', 'author').prefetch_related('tags').filter(is_published=True).\
        order_by('views', 'likes')[:4]
    return {"posts": posts}
