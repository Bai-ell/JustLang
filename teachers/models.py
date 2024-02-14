from django.utils.text import slugify
from django.contrib.auth import get_user_model

from django.db import models
from category.models import LanguageCategory, PriceCategory

from django.db import models

User = get_user_model()

class Post(models.Model):
    owner = models.ForeignKey(User, related_name = 'posts', on_delete = models.CASCADE)

    name = models.CharField(max_length=255, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField("Цена", max_digits=7, decimal_places=2, default=0, null=False)

    language_category = models.ForeignKey(LanguageCategory, on_delete=models.CASCADE, related_name='teachers', verbose_name='Категория по языку')
    price_category = models.ForeignKey(PriceCategory, on_delete=models.CASCADE, related_name='teachers', verbose_name='Категория по цене')
    preview = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='Аватар')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    slug = models.SlugField("URL", unique=True, max_length=150, null=True, blank=True)
 
    
    def save(self, *args, **kwargs):
        if not self.slug:

            self.slug = slugify(self.name)
        super(Post, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Учитель'
        verbose_name_plural = 'Учителя'

        ordering = ['created_at']


    def __str__(self):

        return self.name

    
class PostImages(models.Model):
    title = models.CharField(max_length = 100, blank = True)
    images = models.ImageField(upload_to='images/')
    post = models.ForeignKey(Post, related_name = 'images', on_delete = models.CASCADE)

    def ganerate_name(self):
        from random import randint
        return 'image' + str(self.id) + str(randint(1000, 1_000_000))
    
    def save(self, *args, **kwargs):
        self.title = self.ganerate_name()
        return super(PostImages, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Картинка'
        verbose_name_plural = 'Картинки'

class Favorite(models.Model):
    post = models.ForeignKey(Post, related_name = 'favorites', on_delete = models.CASCADE)
    owner = models.ForeignKey(User, related_name = 'favorites', on_delete = models.CASCADE)

    def __str__(self):
        return f'{self.owner} ==> {self.post}'

class Review(models.Model):
    owner = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='reviews', on_delete=models.CASCADE)
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.owner} ==> {self.post}'

class Rating(models.Model):
    RATING_CHOICES = (
        (1, 'Очень плохо'), 
        (2, 'Плохо'),
        (3, 'Нормально'),
        (4, 'Хорошо'), 
        (5, 'Отлично')
    )
    post = models.ForeignKey(Post, related_name = 'ratings', on_delete = models.CASCADE)
    owner = models.ForeignKey(User, related_name = 'ratings', on_delete = models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices = RATING_CHOICES)
    created_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        unique_together = ['owner', 'post']

    def __str__(self):
        return f'{self.owner} ==> {self.post}'