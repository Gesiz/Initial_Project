from rest_framework.viewsets import ModelViewSet
from apps.goods.models import SKUImage, SKU
from apps.meiduo_admin.serializers.image import SKUImageModelSerializer, SimpleSKUModelSerializer
from apps.meiduo_admin.utils import PageNum

from rest_framework.generics import ListAPIView


class ImageModelViewSet(ModelViewSet):
    queryset = SKUImage.objects.all().order_by('id')
    serializer_class = SKUImageModelSerializer
    pagination_class = PageNum


class SimpleSkuListAPIView(ListAPIView):
    queryset = SKU.objects.all()
    serializer_class = SimpleSKUModelSerializer
