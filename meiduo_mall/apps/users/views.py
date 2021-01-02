import json
import re

from django.shortcuts import render

# Create your views here.


from django.views import View

from apps.users.models import User
from django.http import JsonResponse


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
        # 3.4 验证密码和确认密码一致
        # 3.5 验证手机号是否符合规格

        # 4 保存数据到 Mysql

        # 注意 密码需要加密

        # create_user
        user = User.objects.create_user(
            username=username,
            password=password2,
            mobile=mobile,
        )
        # 5 状态保持
        # request.session['id'] = user.id

        # django 自带后台 后台也是采用的session技术

        # django 实现了 session 状态保持

        from django.contrib.auth import login
        # 参数 1 request 请求对象
        # 参数 2 user 用户信息

        login(request, user)

        # 6 返回响应
        return JsonResponse({'code': 0, 'errmsg': 'ok'})
