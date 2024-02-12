from django.contrib import admin
from .models import PriceCategory, LanguageCategory

# Register your models here.
@admin.register(LanguageCategory)
class LanguageCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "parent", "slug")
    ordering = ("name",)

    def get_prepopulated_fields(self, request, obj=None):
        return {
            "slug": ("name",),
        }
    

@admin.register(PriceCategory)
class PriceCategoryAdmin(admin.ModelAdmin):
    list_display = ("price_range", "slug")
    ordering = ("price_range",)

    def get_prepopulated_fields(self, request, obj=None):
        return {
            "slug": ("price_range",),
        }
