from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy
from .models import Post

class LatestPostsFeed(Feed):
    title = 'Programador Sardinha'
    link = reverse_lazy('blog:post_list')
    description = 'New posts of Programador Sardinha.'

    def items(self):
        return Post.objects.all()[:5]

    def item_title(self, item):
        return item.titulo

    def item_description(self, item):
        return truncatewords(item.conteudo, 30)