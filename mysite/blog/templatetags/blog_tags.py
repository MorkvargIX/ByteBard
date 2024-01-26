import markdown

from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe

from ..models import Post


register = template.Library()


@register.simple_tag
def total_posts():
    return Post.published.count()


@register.filter(name='likes')
def likes(post):
    return post.reactions.filter(reaction='L').count()


@register.filter(name='dislikes')
def dislikes(post):
    return post.reactions.filter(reaction='D').count()


@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))


@register.filter(name='truncate_words')
def truncate_words(value, num_words):
    words = value.split()
    if len(words) > num_words:
        return ' '.join(words[:num_words]) + ' ...'
    else:
        return value
