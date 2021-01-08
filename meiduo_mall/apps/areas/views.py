from django.shortcuts import render
from apps.areas.models import Area
# Create your views here.
from django.views import View
from django.http import JsonResponse
from django.core.cache import cache
import re, json
from utils.views import LoginRequiredJSONMixin
from apps.users.models import Address
from django.contrib.auth import logout


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
        cache.set(pk, sub_list, 24 * 3600)
        return JsonResponse({
            'code': 0,
            'errmsg': 'ok',
            'sub_data': {'subs': sub_list}
        })


class UpdateDestroyAddressView(LoginRequiredJSONMixin, View):
    """修改和删除地址"""

    def delete(self, request, address_id):
        """删除地址"""
        try:
            # 查询要删除的地址
            address = Address.objects.get(id=address_id)

            # 将地址逻辑删除设置为True
            address.is_deleted = True
            address.save()
        except Exception as e:
            return JsonResponse({'code': 400, 'errmsg': '删除地址失败'})

        # 响应删除地址结果
        return JsonResponse({'code': 0, 'errmsg': '删除地址成功'})

    def put(self, request, address_id):
        """修改地址"""
        # 接收参数
        json_dict = json.loads(request.body.decode())
        receiver = json_dict.get('receiver')
        province_id = json_dict.get('province_id')
        city_id = json_dict.get('city_id')
        district_id = json_dict.get('district_id')
        place = json_dict.get('place')
        mobile = json_dict.get('mobile')
        tel = json_dict.get('tel')
        email = json_dict.get('email')

        # 校验参数
        if not all([receiver, province_id, city_id, district_id, place, mobile]):
            return JsonResponse({'code': 400,
                                 'errmsg': '缺少必传参数'})

        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return JsonResponse({'code': 400,
                                 'errmsg': '参数mobile有误'})

        if tel:
            if not re.match(r'^(0[0-9]{2,3}-)?([2-9][0-9]{6,7})+(-[0-9]{1,4})?$', tel):
                return JsonResponse({'code': 400,
                                     'errmsg': '参数tel有误'})
        if email:
            if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
                return JsonResponse({'code': 400,
                                     'errmsg': '参数email有误'})

        # 判断地址是否存在,并更新地址信息
        try:
            Address.objects.filter(id=address_id).update(
                user=request.user,
                title=receiver,
                receiver=receiver,
                province_id=province_id,
                city_id=city_id,
                district_id=district_id,
                place=place,
                mobile=mobile,
                tel=tel,
                email=email
            )
        except Exception as e:

            return JsonResponse({'code': 400, 'errmsg': '更新地址失败'})

        # 构造响应数据
        address = Address.objects.get(id=address_id)
        address_dict = {
            "id": address.id,
            "title": address.title,
            "receiver": address.receiver,
            "province": address.province.name,
            "city": address.city.name,
            "district": address.district.name,
            "place": address.place,
            "mobile": address.mobile,
            "tel": address.tel,
            "email": address.email
        }

        # 响应更新地址结果
        return JsonResponse({'code': 0, 'errmsg': '更新地址成功', 'address': address_dict})


class DefaultAddressView(LoginRequiredJSONMixin, View):
    """设置默认地址"""

    def put(self, request, address_id):
        """设置默认地址"""
        try:
            # 接收参数,查询地址
            address = Address.objects.get(id=address_id)

            # 设置地址为默认地址
            request.user.default_address = address
            request.user.save()
        except Exception as e:
            return JsonResponse({'code': 400, 'errmsg': '设置默认地址失败'})

        # 响应设置默认地址结果
        return JsonResponse({'code': 0, 'errmsg': '设置默认地址成功'})


class UpdateTitleAddressView(LoginRequiredJSONMixin, View):
    """设置地址标题"""

    def put(self, request, address_id):
        """设置地址标题"""
        # 接收参数：地址标题
        json_dict = json.loads(request.body.decode())
        title = json_dict.get('title')

        try:
            # 查询地址
            address = Address.objects.get(id=address_id)

            # 设置新的地址标题
            address.title = title
            address.save()
        except Exception as e:
            return JsonResponse({'code': 400, 'errmsg': '设置地址标题失败'})

        # 4.响应删除地址结果
        return JsonResponse({'code': 0, 'errmsg': '设置地址标题成功'})


class ChangePasswordView(LoginRequiredJSONMixin, View):
    """修改密码"""

    def put(self, request):
        """实现修改密码逻辑"""
        # 接收参数
        dict = json.loads(request.body.decode())
        old_password = dict.get('old_password')
        new_password = dict.get('new_password')
        new_password2 = dict.get('new_password2')

        # 校验参数
        if not all([old_password, new_password, new_password2]):
            return JsonResponse({'code': 400,
                                 'errmsg': '缺少必传参数'})

        result = request.user.check_password(old_password)
        if not result:
            return JsonResponse({'code': 400,
                                 'errmsg': '原始密码不正确'})

        if not re.match(r'^[0-9A-Za-z]{8,20}$', new_password):
            return JsonResponse({'code': 400,
                                 'errmsg': '密码最少8位,最长20位'})

        if new_password != new_password2:
            return JsonResponse({'code': 400,
                                 'errmsg': '两次输入密码不一致'})

        # 修改密码
        try:
            request.user.set_password(new_password)
            request.user.save()
        except Exception as e:

            return JsonResponse({'code': 400,
                                 'errmsg': '修改密码失败'})

        # 清理状态保持信息
        logout(request)

        response = JsonResponse({'code': 0,
                                 'errmsg': 'ok'})

        response.delete_cookie('username')

        # # 响应密码修改结果：重定向到登录界面
        return response
