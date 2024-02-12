from rest_framework import serializers
from .models import LanguageCategory, PriceCategory

class LanguageCategorySerializer(serializers.ModelSerializer):
    parent_name = serializers.ReadOnlyField(source = 'parent.name')

    class Meta:
        model = LanguageCategory
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        parents = instance.children.all()
        if parents:
            representation['children'] = LanguageCategorySerializer(
                parents, many = True
            ).data
        return representation
    
class PriceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceCategory
        fields = ['id', 'price_range', 'slug']