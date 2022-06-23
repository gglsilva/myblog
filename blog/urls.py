from django.urls import path, include
from .feeds import LatestPostsFeed
from . import views

app_name = 'blog'

urlpatterns = [
    #path('', views.home, name='home'),
    path('', views.post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
    path('search_results/', views.post_search, name='post_search'),
]