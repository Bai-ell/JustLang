from django.contrib import admin

from .models import Post, PostImages

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("name", "language_category", "price_category",  "slug", "id")
    ordering = ("id",)

    def get_prepopulated_fields(self, request, obj=None):
        return {
            "slug": ("name",),
        }
    
admin.site.register(PostImages)
