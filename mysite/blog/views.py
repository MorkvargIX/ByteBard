from django.http import JsonResponse
from django.db.models import Count, F, Q
from django.utils.text import slugify
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.postgres.search import SearchVector, SearchRank, SearchQuery
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from taggit.models import Tag

from .models import Post, Reaction, Subscriber, User
from .forms import SubscriptionForm, CommentForm, SearchFrom, UserCreationForm, UserLoginForm, CreationPostForm


def post_list(request, tag_slug=None, author=None):
    query = request.GET.get('query', None)

    all_posts = Post.published.all()
    all_tags = Tag.objects.all()

    if author:
        all_posts = Post.published.filter(author__username=author)

    if query:
        search_form = SearchFrom(request.GET)
        if search_form.is_valid():
            query = search_form.cleaned_data['query']
            all_posts = Post.published.annotate(
                title_search=SearchVector('title'),
                body_search=SearchVector('body')
            ).annotate(
                search_rank_title=SearchRank(F('title_search'), SearchQuery(query)),
                search_rank_body=SearchRank(F('body_search'), SearchQuery(query))
            ).filter(
                Q(search_rank_title__gt=0) | Q(search_rank_body__gt=0)
            ).order_by('-search_rank_title', '-search_rank_body')

    paginator = Paginator(all_posts, 6)
    best_blogs = Post.best_posts.all()[:5]
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        all_posts = all_posts.filter(tags__in=[tag])
        paginator = Paginator(all_posts, 6)

    page_number = request.GET.get('page', 1)
    try:
        all_posts = paginator.page(page_number)
    except PageNotAnInteger:
        all_posts = paginator.page(1)
    except EmptyPage:
        all_posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {
        'all_posts': all_posts,
        'tag': tag,
        'all_tags': all_tags,
        'best_blogs': best_blogs,
        'query': query,
    })


def post_detail(request, id, slug):
    subscribed_message = False

    recent_posts = Post.published.all()[:5]
    best_blogs = Post.best_posts.all()[:5]
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED, id=id, slug=slug)

    if request.user.is_authenticated:
        subscription = Subscriber.objects.filter(username=request.user.username, author=post.author)
        if subscription:
            subscribed_message = True

    tags = post.tags.names()
    same_posts = Post.objects.filter(tags__name__in=tags).exclude(pk=post.pk).distinct()

    comments = post.comments.filter(active=True)
    comment_form = CommentForm()
    subscribe_form = SubscriptionForm()
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    return render(
        request,
        'blog/post/detail.html',
        {
            'post': post,
            'comments': comments,
            'comment_form': comment_form,
            'subscribe_form': subscribe_form,
            'similar_posts': similar_posts,
            'recent_posts': recent_posts,
            'best_blogs': best_blogs,
            'subscribed_message': subscribed_message,
            'same_posts': same_posts,
        }
    )


@login_required(login_url='blog:user_login')
def post_create(request):
    recent_posts = Post.published.all()[:5]
    if request.method == 'POST':
        form = CreationPostForm(data=request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.slug = slugify(post.title)
            post.save()
            tags = form.cleaned_data['tags']
            for tag in tags:
                tag_instance, created = Tag.objects.get_or_create(name=tag)
                post.tags.add(tag_instance)
            post.save()
    form = CreationPostForm()
    return render(request, 'blog/post/create.html', {'form': form, 'recent_posts': recent_posts})


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


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('blog:post_list')
    else:
        form = UserLoginForm()
    return render(request, 'blog/post/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('blog:post_list')


@login_required(login_url='blog:user_login')
@require_POST
def newsletter_subscription(request, post_id):
    email_form = SubscriptionForm(data=request.POST)
    post = get_object_or_404(Post, id=post_id)
    author = post.author
    current_user = get_object_or_404(User, username=request.user.username)
    if current_user and email_form.is_valid() and author != current_user:
        subscription = Subscriber(username=current_user.username, email=email_form.cleaned_data['email'], author=author)
        subscription.save()
        return JsonResponse({'Success': 'You have successfully subscribed to the user newsletter!'})
    return JsonResponse({'Error': 'Something went wrong, failed to subscribe to the user\'s newsletter!'})


@login_required
@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    user = request.user
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
        return JsonResponse({'username': user.username, 'publish': comment.created})
    return JsonResponse({'error': 'Invalid form data'})


@require_POST
def post_reaction(request, post_id, choice):
    if not request.user.is_authenticated:
        return JsonResponse({'redirect_url': '/login/'})

    post = get_object_or_404(Post, pk=post_id)
    user = request.user
    reaction = Reaction.objects.filter(post=post, user=user)

    if not reaction:
        reaction = Reaction(reaction=choice, post=post, user=user)
        reaction.save()
    elif reaction and reaction.values('reaction')[0]['reaction'] != choice:
        reaction.update(reaction=choice)
    elif reaction and reaction.values('reaction')[0]['reaction'] == choice:
        reaction.delete()

    likes_count = post.reactions.filter(reaction='L').count()
    dislikes_count = post.reactions.filter(reaction='D').count()
    return JsonResponse({'likes_count': likes_count, 'dislikes_count': dislikes_count})
