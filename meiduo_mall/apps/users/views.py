import json
import re

from django.shortcuts import render

# Create your views here.


from django.views import View
from apps.users.models import User
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.users.models import Address


class UsernameCountView(View):
    # usernames/<username>/count
    def get(self, request, username):
        count = User.objects.filter(username=username).count()
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'count': count})


class MobileCountView(View):

    def get(self, request, mobile):
        count = User.objects.filter(mobile=mobile).count()
        print(count)
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'count': count})


class RegisterView(View):

    def post(self, request):
        # 1 接收请求
        body = request.body
        body_str = body.decode()
        data = json.loads(body_str)
        # 2 提取参数
        username = data.get('username')
        password = data.get('password')
        password2 = data.get('password2')
        mobile = data.get('mobile')
        allow = data.get('allow')

        # 3 验证参数
        # 3.1 提取的5个变量都必须有值
        if not all([username, password, password2, mobile, allow]):
            return JsonResponse({'code': 400, 'errmsg': '参数不全'})

        # 3.2 验证用户名是否符合规则
        if not re.match('[a-zA-Z0-9_-]{5,20}', username):
            return JsonResponse({'code': 400, 'errmsg': '用户名不满足条件'})
        # 3.3 验证密码是否符合规则
        if not re.match('[a-zA-Z0-9]{8,20}', password):
            return JsonResponse({'code': 400, 'errmsg': 'password格式有误'})

        # 3.4 验证密码和确认密码一致
        if password != password2:
            return JsonResponse({'code': 400, 'errmsg': '两次输入不一致'})
        # 3.5 验证手机号是否符合规格
        if not re.match('1[3-9]\d{9}', mobile):
            return JsonResponse({'code': 400, 'errmsg': 'mobile格式有误'})
        # 4 保存数据到 Mysql
        if not allow:
            return JsonResponse({'code': 400, 'errmsg': 'allow格式有误'})
        # 注意 密码需要加密

        # create_user
        try:
            user = User.objects.create_user(
                username=username,
                password=password2,
                mobile=mobile,
            )
        except Exception as e:
            return JsonResponse({'code': 400, 'errmsg': '注册失败'})
        # 5 状态保持
        # request.session['id'] = user.id

        # django 自带后台 后台也是采用的session技术

        # django 实现了 session 状态保持

        from django.contrib.auth import login
        # 参数 1 request 请求对象
        # 参数 2 user 用户信息

        login(request, user)

        # 6 返回响应
        return JsonResponse({'code': 0, 'errmsg': '注册成功'})


class LoginView(View):
    def post(self, request):
        """
        :param request:
        :return:
        """
        data = json.loads(request.body.decode())
        # 1 接收请求数据

        # 2 提取数据

        username = data.get('username')
        password = data.get('password')
        rememberd = data.get('remembered')
        # 3 验证参数
        if not all([username, password]):
            pass

        if re.match(r'1[3-9]\d{9}', username):
            User.USERNAME_FIELD = 'mobile'
        else:
            User.USERNAME_FIELD = 'username'

        # 4 认证登录用户

        user = authenticate(username=username, password=password)
        if user is None:
            return JsonResponse({'code': 400, 'errmsg': '密码不正确'})
        # 5 状态保持

        login(request, user)

        # 6 要根据是否记住登录
        if rememberd:
            request.session.set_expiry(None)
        else:
            request.session.set_expiry(0)

        response = JsonResponse({'code': 0, 'errmsg': 'ok'})
        # 7 返回响应
        response.set_cookie('username', username, max_age=14 * 24 * 3600)
        return response


class LogoutView(View):

    def delete(self, request):
        from django.contrib.auth import logout
        logout(request)
        response = JsonResponse({'code': 0, 'errmsg': '退出成功'})
        response.delete_cookie('username')
        return response


from utils.views import LoinRequiredJSONMixin


class UserInfoVIew(LoinRequiredJSONMixin, View):
    def get(self, request):
        user = request.user
        user_info = {
            'username': user.username,
            'mobile': user.mobile,
            'email': user.email,
            'email_active': user.email_active,  # 明天才讲 email_active 先给一个固定值
        }
        print(user_info)
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'info_data': user_info})


class EmailView(View):
    def put(self, request):
        # 1 判断用户是否登录

        # 2 接收请求
        data = json.loads(request.body.decode())
        # 3 提取参数
        email = data.get('email')
        # 4 验证参数

        # 5 更新用户信息
        user = request.user
        user.email = email
        user.save()

        # 6 发送激活文件
        from apps.users.utils import generic_user_id
        token = generic_user_id(user.id)
        verify_url = 'http://www.meiduo.site:8080/success_verify_email.html?token=%s' % token
        html_message = '<p>尊敬的用户您好！</p>' \
                       '<p>感谢您使用美多商城。</p>' \
                       '<p>您的邮箱为：%s 。请点击此链接激活您的邮箱：</p>' \
                       '<p><a href="%s">%s<a></p>' % (email, verify_url, verify_url)

        from celery_tasks.email.tasks import celery_send_email
        print(email)
        celery_send_email.delay(email, html_message)

        # 7 返回响应
        return JsonResponse({'code': 0, 'errmsg': 'ok'})


class VerifyEmailView(View):
    def put(self, request):
        # 1 接收请求
        data = request.GET
        token = data.get('token')
        from apps.users.utils import check_user_id
        user_id = check_user_id(token)
        print(user_id)
        if user_id is None:
            return JsonResponse({'code': 400, 'errmsg': '链接失效'})
        print(111111111111111111111)
        # 有可能换浏览器
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'code': 400, 'errmsg': '链接失效'})
        print(111111111111111111111)
        user.email_active = True
        user.save()
        print(22222222222222222222)
        return JsonResponse({'code': 0, 'errmsg': 'ok'})


##################地址管理##########################

class CreateAddressView(LoinRequiredJSONMixin, View):

    def post(self, request):
        json_dict = json.loads(request.body.decode())
        receiver = json_dict.get('receiver')
        province_id = json_dict.get('province_id')
        city_id = json_dict.get('city_id')
        district_id = json_dict.get('district_id')
        place = json_dict.get('place')
        mobile = json_dict.get('mobile')
        tel = json_dict.get('tel')
        email = json_dict.get('email')

        # # 校验参数
        # if not all([receiver, province_id, city_id, district_id, place, mobile]):
        #     return HttpResponseBadRequest('缺少必传参数')
        # if not re.match(r'^1[3-9]\d{9}$', mobile):
        #     return HttpResponseBadRequest('参数mobile有误')
        # if tel:
        #     if not re.match(r'^(0[0-9]{2,3}-)?([2-9][0-9]{6,7})+(-[0-9]{1,4})?$', tel):
        #         return HttpResponseBadRequest('参数tel有误')
        # if email:
        #     if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
        #         return HttpResponseBadRequest('参数email有误')

        try:
            address = Address.objects.create(
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

            # 设置默认地址
            if not request.user.default_address:
                request.user.default_address = address
                request.user.save()
        except Exception as e:
            return JsonResponse({'code': 400, 'errmsg': '新增地址失败'})

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

        # 响应保存结果
        return JsonResponse({'code': 0, 'errmsg': '新增地址成功', 'address': address_dict})


class AddressesListView(LoinRequiredJSONMixin, View):

    def get(self, request):
        """提供地址管理界面
        """
        # 获取所有的地址:
        addresses = Address.objects.filter(user=request.user,
                                           is_deleted=False)

        # 创建空的列表
        address_dict_list = []
        # 遍历
        for address in addresses:
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

            # 将默认地址移动到最前面
            default_address = request.user.default_address
            if default_address.id == address.id:
                # 查询集 addresses 没有 insert 方法
                address_dict_list.insert(0, address_dict)
            else:
                address_dict_list.append(address_dict)

        default_id = request.user.default_address_id

        return JsonResponse({'code': 0,
                             'errmsg': 'ok',
                             'addresses': address_dict_list,
                             'default_address_id': default_id})