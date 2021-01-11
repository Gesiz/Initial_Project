import json

from django.shortcuts import render

# Create your views here.
from utils.views import LoginRequiredJSONMixin
from django.views import View
from apps.goods.models import SKU
from django.http import JsonResponse
from django_redis import get_redis_connection


class CartsView(View):

    def post(self, request):
        user = request.user
        data = json.loads(request.body.decode())
        sku_id = data.get('sku_id')
        count = data.get('count')

        try:
            sku = SKU.objects.get(id=sku_id)
        except Exception:
            return JsonResponse({})

        try:
            count = int(count)
        except Exception:
            count = 1

        redis_cli = get_redis_connection('carts')
        redis_cli.hset(f'carts_{user.id}', sku_id, count)
        redis_cli.sadd(f'select_{user.id}', sku_id)
        return JsonResponse({'code': 0, 'errmsg': 'ok'})

    def get(self, request):
        user = request.user

        redis_cli = get_redis_connection('carts')

        sku_id_counts = redis_cli.hgetall(f'carts_{user.id}')

        selected_ids = redis_cli.smembers(f'select_{user.id}')

        ids = sku_id_counts.keys()
        carts_sku = []
        for id in ids:
            sku = SKU.objects.get(id=id)

            carts_sku.append({
                'id': sku.id,
                'name': sku.name,
                'price': sku.price,
                'default_image_url': sku.default_image.url,
                'count': int(sku_id_counts[id]),
                'selected': id in selected_ids,
                'amount': sku.price * int(sku_id_counts[id]),
            })
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'cart_skus': carts_sku})

    def put(self, request):

        user = request.user

        data = json.loads(request.body.decode())

        sku_id = data.get('sku_id')
        count = data.get('count')
        selected = data.get('selected')

        try:
            sku = SKU.objects.get(id=sku_id)
        except SKU.DoesNotExist:
            return JsonResponse({'code': 400, 'errmsg': '没有此商品'})

        redis_cli = get_redis_connection('carts')

        redis_cli.hset('carts_%s' % user.id, sku_id, count)

        if selected:
            redis_cli.sadd(f'select_{user.id}', sku_id)
        else:
            redis_cli.srem('select_%s' % user.id, sku_id)

        cart_sku = {
            'id': sku_id,
            'count': count,
            'selected': selected,
            'name': sku.name,
            'default_image_url': sku.default_image.url,
            'price': sku.price,
            'amount': sku.price * count,
        }
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'cart_sku': cart_sku})

    def delete(self, request):
        user = request.user

        data = json.loads(request.body.decode())

        sku_id = data.get('sku_id')

        try:
            SKU.objects.get(id=sku_id)
        except Exception:
            return JsonResponse({'code': 400, 'errmsg': 'No'})

        redis_cli = get_redis_connection('carts')

        redis_cli.hdel(f'cart_{user.id}', sku_id)

        redis_cli.srem(f'select_{user.id}', sku_id)

        return JsonResponse({'code': 400, 'errmsg': 'ok'})
