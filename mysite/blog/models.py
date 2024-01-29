from django.db import models
from django.db.models import F, Count, ExpressionWrapper, Q
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
from martor.models import MartorField


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class BestPostsManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(status=Post.Status.PUBLISHED)
            .annotate(
                total_comments=Count('comments', distinct=True),
                total_likes=Count('reactions', filter=Q(reactions__reaction='L'), distinct=True),
                total_dislikes=Count('reactions', filter=Q(reactions__reaction='D'), distinct=True)
            )
            .annotate(
                total_score=ExpressionWrapper(
                    F('total_comments') + F('total_likes') - F('total_dislikes'),
                    output_field=models.IntegerField()
                )
            )
            .order_by('-total_score')
        )


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = MartorField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    objects = models.Manager()
    published = PublishedManager()
    best_posts = BestPostsManager()
    tags = TaggableManager()

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.slug, self.id])


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return f'{self.id}. Comment by {self.author} on {self.post}'


class Reaction(models.Model):
    class Options(models.TextChoices):
        LIKE = 'L', 'Like'
        DISLIKE = 'D', 'Dislike'

    reaction = models.CharField(max_length=1, choices=Options.choices)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reactions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reactions')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
            models.Index(fields=['post']),
        ]
        unique_together = [['post', 'user']]

    def __str__(self):
        if self.reaction == 'L':
            return f'{self.user.username} liked: post - {self.post.title}'
        return f'{self.user.username} disliked: post - {self.post.title}'


class Subscriber(models.Model):
    username = models.CharField(max_length=150)
    email = models.EmailField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscribers')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return f'{self.username} subscribed on {self.author.username}\' posts'
