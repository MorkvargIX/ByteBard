from django.urls import path, include

from . import views
from .feeds import LatestPostsFeed

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    path('<slug:slug>/<int:id>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/subscription/', views.newsletter_subscription, name='newsletter_subscription'),
    path('<int:post_id>/comment/', views.post_comment, name='post_comment'),
    path('<int:post_id>/<str:choice>/reaction/', views.post_reaction, name='post_reaction'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
    path('registration/', views.user_registration, name='user_registration'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('create/', views.post_create, name='post_create'),
]
