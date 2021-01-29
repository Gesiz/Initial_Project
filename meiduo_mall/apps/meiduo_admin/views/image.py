from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from apps.goods.models import SKUImage, SKU
from apps.meiduo_admin.serializers.image import SKUImageModelSerializer, SimpleSKUModelSerializer
from apps.meiduo_admin.utils import PageNum, PutImage

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

        image_url = PutImage(upload_image.read())
        print(image_url)
        new_image = SKUImage.objects.create(
            sku_id=sku_id,
            image=image_url
        )
        return Response({
            'id': new_image.id,
            'image': new_image.image.url,
        }, status=201)

    def update(self, request, *args, **kwargs):
        # 1 接收数据
        data = request.data
        # 2 提取数据
        sku_id = data.get('sku')
        new_upload_image = data.get('image')
        # 3 验证数据

        # 4 七牛云上传新图片
        # request.FILES.get('image').read()

        new_image_url = PutImage(data=data.get('image'))
        # 5 数据更新
        print(new_image_url)
        pk = self.kwargs.get('pk')
        new_image = SKUImage.objects.get(id=pk)
        new_image.image = new_image_url
        new_image.save()
        # 6 返回响应
        return Response(
            {
                'id': new_image.id,
                'image': new_image.image.url,
                'sku': sku_id
            }
        )


class SimpleSkuListAPIView(ListAPIView):
    queryset = SKU.objects.all()
    serializer_class = SimpleSKUModelSerializer
