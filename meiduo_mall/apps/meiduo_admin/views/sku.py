from rest_framework.viewsets import ModelViewSet
from apps.goods.models import SKU
from apps.meiduo_admin.serializers.sku import SKUModelSerializer
from apps.meiduo_admin.utils import PageNum
from rest_framework.response import Response


class SKUModelViewSet(ModelViewSet):
    queryset = SKU.objects.all()
    serializer_class = SKUModelSerializer
    pagination_class = PageNum


"""
获取三级分类数据
一级分类 none id(1-37)
二级分类 id(38-114)
三级分类 id(115~)
"""

from apps.goods.models import GoodsCategory

from rest_framework.views import APIView

from apps.meiduo_admin.serializers.sku import GoodsCategoryModelSerializer, \
    SimpleSPUModelSerializer


class GoodCategoryAPIView(APIView):
    def get(self, request):
        gcs = GoodsCategory.objects.filter(subs=None)
        s = GoodsCategoryModelSerializer(instance=gcs, many=True)
        return Response(s.data)


from apps.goods.models import SPU
from rest_framework.generics import ListAPIView


class SPUSimpleListAPIView(ListAPIView):
    queryset = SPU.objects.all()
    serializer_class = SimpleSPUModelSerializer


from apps.goods.models import SPUSpecification
from apps.goods.models import SpecificationOption
from apps.meiduo_admin.serializers.sku import SPUSpecModelSerializer


class GoodSpecsAPIView(APIView):
    def get(self, request, spu_id):
        # 根据 spu_id 查询规格信息
        specs = SPUSpecification.objects.filter(spu_id=spu_id)
        s = SPUSpecModelSerializer(instance=specs, many=True)
        return Response(s.data)
