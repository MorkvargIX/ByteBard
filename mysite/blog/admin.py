from django.contrib import admin
from .models import Post, Comment, Like, Dislike


@admin.register(Post)
class AdminPost(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status']
    list_filter = ['status', 'created', 'publish', 'author']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    ordering = ['status', 'publish']


@admin.register(Comment)
class AdminComment(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']


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
