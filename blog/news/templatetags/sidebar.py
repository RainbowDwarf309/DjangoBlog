from django import template
from news.models import Post, Tag

register = template.Library()


@register.inclusion_tag('news/tags.html')
def get_tags():
    tags = Tag.objects.all()[:30]
    return {"tags": tags}




