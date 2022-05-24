from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


class Post(models.Model):
    STATUS_CHOICES = (
        ('rascunho', 'Rascunho'),
        ('publicado', 'Publicado'),
    )
    titulo = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publicado')
    autor = models.ForeignKey(User,on_delete=models.CASCADE,related_name='blog_posts')
    imagem = models.ImageField(upload_to='blog/%Y/%m/%d', blank=True)
    resumo = models.CharField(max_length=250)
    conteudo = RichTextUploadingField()
    publicado = models.DateTimeField(default=timezone.now)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='rascunho')

    class Meta:
        ordering = ('-publicado',)

    def __str__(self):
        return self.titulo

    
    def get_absolute_url(self):
        return reverse('blog:post_detail',
                        args=[self.publicado.year,
                        self.publicado.month,
                        self.publicado.day, 
                        self.slug])