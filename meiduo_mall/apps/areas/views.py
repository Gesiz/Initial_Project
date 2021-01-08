from django.shortcuts import render
from apps.areas.models import Area
# Create your views here.
from django.views import View
from django.http import JsonResponse
from django.core.cache import cache


class ProvinceView(View):

    def get(self, request):
        province_list = cache.get('province')
        if province_list is None:

            provinces = Area.objects.filter(parent=None)
            province_list = []
            for item in provinces:
                province_list.append({
                    'id': item.id,
                    'name': item.name
                })
            cache.set('province', province_list, 24 * 3600)

        return JsonResponse({'code': 0, 'errmsg': 'ok', 'province_list': province_list})


class SubAreaView(View):

    def get(self, request, pk):
        sub_list = cache.get(pk)
        if sub_list is None:
            sub_areas = Area.objects.filter(parent_id=pk)
            sub_list = []
            for item in sub_areas:
                sub_list.append({
                    'id': item.id,
                    'name': item.name,
                })
        cache.set(pk,sub_list,24*3600)
        return JsonResponse({
            'code': 0,
            'errmsg': 'ok',
            'sub_data': {'subs': sub_list}
        })
