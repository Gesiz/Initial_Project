from django.shortcuts import render
from apps.areas.models import Area
# Create your views here.
from django.views import View
from django.http import JsonResponse
class ProvinceView(View):

    def get(self,request):
        provinces = Area.objects.filter(parent=None)
        province_list = []
        for item in provinces:
            province_list.append({
                'id':item.id,
                'name':item.name
            })

        return JsonResponse({'code':0,'errmsg':'ok','province_list':province_list})

class SubAreaView(View):

    def get(self,request,pk):
        pass
