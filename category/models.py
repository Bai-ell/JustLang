from django.db import models
from django.utils.text import slugify

class LanguageCategory(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    slug = models.SlugField("URL", unique=True, max_length=150, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(LanguageCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Категория по языку'
        verbose_name_plural = 'Категории по языку'

    
class PriceCategory(models.Model):
    price_range = models.CharField(max_length=50, unique=True)
    slug = models.SlugField("URL", unique=True, max_length=150, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.price_range)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.price_range
    
    class Meta:
        verbose_name = 'Категория по ценам'
        verbose_name_plural = 'Категории по ценам'