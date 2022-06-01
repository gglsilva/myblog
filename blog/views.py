from hashlib import new
from xml.etree.ElementTree import Comment
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from taggit.models import Tag
from .forms import EmailPostForm, CommentForm
from .models import Post
from django.db.models import Count


def post_list(request, tag_slug=None):
    post_list = Post.objects.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])

    paginator = Paginator(post_list, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages) 
    return render(request, 'blog/post/list.html', {'page': page,
                                                   'posts': posts,
                                                   'tag': tag})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                   status='publicado',
                                   publicado__year=year,
                                   publicado__month=month,
                                   publicado__day=day)
    # Lista de comentários para o post atual
    comments = post.comments.filter(comentario_aprovado=True)
    new_comment = None
    if request.method == 'POST':
        # Um comentario foi postado
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
    # Lista postagens relacionadas
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.objects.filter(tags__in=post_tags_ids)\
                                  .exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
                                .order_by('-same_tags','-publicado')[:4]
    return render(request, 'blog/post/detail.html', {'post': post,
                                                    'comments': comments,
                                                    'new_comment': new_comment,
                                                    'comment_form': comment_form,
                                                    'similar_posts': similar_posts})


def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='publicado')
    sent = False

    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.titulo}"
            message = f"Read {post.titulo} at {post_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True

    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})
