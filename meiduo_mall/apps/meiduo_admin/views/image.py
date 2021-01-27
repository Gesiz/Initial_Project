from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from apps.goods.models import SKUImage, SKU
from apps.meiduo_admin.serializers.image import SKUImageModelSerializer, SimpleSKUModelSerializer
from apps.meiduo_admin.utils import PageNum

from rest_framework.generics import ListAPIView


class ImageModelViewSet(ModelViewSet):
    queryset = SKUImage.objects.all().order_by('id')
    serializer_class = SKUImageModelSerializer
    pagination_class = PageNum

    def create(self, request, *args, **kwargs):
        upload_image = request.FILES.get('image')

        data = request.data

        sku_id = data.get('sku')

        try:
            sku = SKU.objects.get(id=sku_id)
        except SKU.DoesNotExist:
            return Response({'msg': '没有此商品'})

        image_url = ''

        new_image = SKUImage.objects.create(
            sku_id=sku_id,
            image=image_url
        )
        return Response({
            'id': new_image.id,
            'image': new_image.image.url,
        }, status=201)


class SimpleSkuListAPIView(ListAPIView):
    queryset = SKU.objects.all()
    serializer_class = SimpleSKUModelSerializer
