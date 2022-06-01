from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
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

    tags = TaggableManager()

    class Meta:
        ordering = ('-publicado',)

    def __str__(self):
        return self.titulo

    def comentarios_aprovados(self):
        return self.comments.filter(omentario_aprovado=True)

    
    def get_absolute_url(self):
        return reverse('blog:post_detail',
                        args=[self.publicado.year,
                        self.publicado.month,
                        self.publicado.day, 
                        self.slug])


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    nome = models.CharField(max_length=80)
    email = models.EmailField()
    conteudo = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    comentario_aprovado = models.BooleanField(default=False)

    class Meta:
        ordering = ('criado_em',)

    def approve(self):  
        self.comentario_aprovado = True
        self.save()
        
    def __str__(self):
        return f'Comment by {self.nome} on {self.post}'