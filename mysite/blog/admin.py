from django.contrib import admin
from django.db import models
from .models import Post, Comment, Like, Dislike
from martor.widgets import AdminMartorWidget


@admin.register(Post)
class AdminPost(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status']
    list_filter = ['status', 'created', 'publish', 'author']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    ordering = ['status', 'publish']
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }


@admin.register(Comment)
class AdminComment(admin.ModelAdmin):
    list_display = ['author', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['author', 'body']


@admin.register(Like)
class AdminLike(admin.ModelAdmin):
    list_display = ['user', 'post', 'created']
    list_filter = ['post', 'user']
    search_fields = ['created', 'post']


@admin.register(Dislike)
class AdminDislike(admin.ModelAdmin):
    list_display = ['user', 'post', 'created']
    list_filter = ['post', 'user']
    search_fields = ['created', 'post']

