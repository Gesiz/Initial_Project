import json
import re

from django.shortcuts import render

# Create your views here.


from django.views import View
from apps.users.models import User
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin


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
            'email_activate': user.email_active,  # 明天才讲 email_active 先给一个固定值
        }
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'info_data': user_info})
