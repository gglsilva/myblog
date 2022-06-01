from django import template
from ..models import Post
from django.db.models import Count
from taggit.models import Tag
from django.utils.safestring import mark_safe
import markdown


register = template.Library()

@register.simple_tag
def total_posts():
    return Post.objects.count()


@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.objects.order_by('-publicado')[:count]
    return {'latest_posts': latest_posts}


@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.objects.annotate(
        total_comments=Count('comments')
        ).order_by('-total_comments')[:count]


@register.inclusion_tag('blog/post/posts_tags.html')
def show_posts_tags():
    tags = Tag.objects.all()
    return {'tags': tags}


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))