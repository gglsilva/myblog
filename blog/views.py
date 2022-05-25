from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post


def post_list(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages) 
    return render(request, 'blog/post/list.html', {'page': page,
                                                   'posts': posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                   status='publicado',
                                   publicado__year=year,
                                   publicado__month=month,
                                   publicado__day=day)
    return render(request, 'blog/post/detail.html', {'post': post})
