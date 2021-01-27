from apps.goods.models import SKUImage
from rest_framework import serializers


class SKUImageModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SKUImage
        # fields = '__all__'
        fields = ['id', 'sku', 'image']


from apps.goods.models import SKU


class SimpleSKUModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SKU
        fields = ['id', 'name']
