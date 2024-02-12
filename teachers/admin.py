from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "language_category", "price_category",  "slug")
    ordering = ("title",)

    def get_prepopulated_fields(self, request, obj=None):
        return {
            "slug": ("title",),
        }
    
