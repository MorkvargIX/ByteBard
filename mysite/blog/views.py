from django.conf import settings
from django.db.models import Count
from django.core.mail import send_mail
from django.contrib.auth import login
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.postgres.search import SearchVector
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from taggit.models import Tag

from .models import Post
from .forms import EmailPostForm, CommentForm, SearchFrom, UserCreationForm


def post_list(request, tag_slug=None):
    all_posts = Post.published.all()
    all_tags = Tag.objects.all()
    last_posts = all_posts[:2]
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        all_posts = all_posts.filter(tags__in=[tag])
    paginator = Paginator(all_posts[2:], 6)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {
        'posts': posts,
        'tag': tag,
        'all_tags': all_tags,
        'last_posts': last_posts
    })


def post_detail(request, id, slug):
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED, id=id, slug=slug)
    comments = post.comments.filter(active=True)
    form = CommentForm()
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    return render(
        request,
        'blog/post/detail.html',
        {
            'post': post,
            'comments': comments,
            'form': form,
            'similar_posts': similar_posts
        }
    )


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)

    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f'{cd['name']} recommends you read {post.title}'
            message = f'Read {post.title} at {post_url}\n\n{cd['name']}\'s comments: {cd['comment']}'
            send_mail(subject, message, settings.EMAIL_HOST_USER, [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return render(request, 'blog/post/comment.html', {
        'post': post,
        'form': form,
        'comment': comment
    })


def post_search(request):
    form = SearchFrom()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchFrom(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.published.annotate(search=SearchVector('title', 'body'),).filter(search=query)
    return render(request, 'blog/post/search.html', {'form': form, 'query': query, 'results': results})


def user_registration(request):
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('blog:post_list')
    else:
        form = UserCreationForm()
    return render(request, 'blog/post/registration.html', {'form': form})


