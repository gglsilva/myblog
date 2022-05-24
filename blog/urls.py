from django.urls import path, include
from . import views

urlpatterns = [
    #path('', views.home, name='home'),
    path('', views.post_list, name='post_list'),
]