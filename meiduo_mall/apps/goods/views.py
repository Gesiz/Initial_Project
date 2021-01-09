from django.shortcuts import render
from django.views import View
from utils.goods import *
from django.http import JsonResponse

from apps.goods.models import GoodsCategory
from apps.goods.models import SKU


# Create your views here.
class IndexView(View):

    def get(self, request):
        """
        1. 获取分类数据
        2. 获取首页数据
        3. 组织数据 进行渲染
        :param request:
        :return:
        """
        # 1. 获取分类数据
        categories = get_categories()
        # 2. 获取首页数据
        contents = get_contents()
        # 3. 组织数据 进行渲染
        # 注意: key必须是这2个 因为模板中已经写死
        context = {
            'categories': categories,
            'contents': contents
        }
        return render(request, 'index.html', context)


# #######################################列表首页###################
class ListView(View):
    def get(self, request, category_id):
        # 1 接收参数
        data = request.GET
        # 2 提取参数
        page = data.get('page')
        page_size = data.get('page_size')
        ordering = data.get('ordering')
        # 3 根据分类ID查询分类数据

        try:
            category = GoodsCategory.objects.get(id=category_id)
        except GoodsCategory.DoesNotExist:
            return JsonResponse({'code': 400, 'errmsg': '没有此分类'})
        # 4 验证参数
        # 4.1 page 整数
        # 4.2 page_size 整数
        # 4.3 ordering 只能是 create_time , price, sales
        # 5 查询数据

        skus = SKU.objects.filter(category=category,
                                  is_launched=True).order_by(ordering)
        # 6 分页数据
        from django.core.paginator import Paginator

        paginator = Paginator(skus, page_size)

        page_skus = paginator.page(page)

        total_num = paginator.num_pages

        # 7 将对象列表转换为字典列表

        sku_list = []
        for item in page_skus:
            sku_list.append(
                {
                    'id': item.id,
                    'name': item.name,
                    'price': item.price,
                    'default_image_url': item.default_image.url

                }
            )

        # 8 返回对象
        from utils.goods import get_breadcrumb
        breadcrumb = get_breadcrumb(category)
        return JsonResponse({
            'code': 0,
            'errmsg': 'ok',
            'list': sku_list,
            'count': total_num,
            'breadcrumb': breadcrumb,
        })


class HotView(View):
    def get(self, request, category_id):
        # 1 接收参数
        # 2 根据分类id查询分类数据
        # 3 查询SKU数据条件就是 分类
        # 排序 根据销量 倒叙 获取两条数据
        # 4 将对象列表转换为字典列表
        # 5 返回对象
        try:
            category = GoodsCategory.objects.get(id=category_id)
        except GoodsCategory.DoesNotExist:
            return JsonResponse({'code': 400, 'errmsg': '没有此分类'})

        skus = SKU.objects.filter(category=category, is_launched=True).order_by('-sales')[0:2]

        sku_list = []
        for item in skus:
            sku_list.append(
                {
                    'id': item.id,
                    'name': item.name,
                    'price': item.price,
                    'default_image_url': item.default_image.url
                }
            )
        return JsonResponse({
            'code': 0,
            'errmsg': 'ok',
            'hot_skus': sku_list,
        })


from utils.goods import *


########################
class DetailView(View):
    def get(self, request, sku_id):
        # 1 获取商品id
        try:
            sku = SKU.objects.get(id=sku_id)
        except SKU.DoserNotExist:
            return JsonResponse({'code': 400, 'errmsg': '商品不存在'})

        # 2 根据商品 id 查询商品信息
        # 3 获取分类数据
        categories = get_categories()
        # 4 获取面包屑数据
        breadcrumb = get_breadcrumb(sku.category)
        # 5 获取规格和规格选项数据
        specs = get_goods_specs(sku)
        # 6 组织数据
        context = {
            'sku': sku,
            'categories': categories,
            'breadcrumb': breadcrumb,
            'specs': specs,
        }

        return render(request, 'detail.html', context=context)
