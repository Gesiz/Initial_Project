import json
import re

from django.shortcuts import render

# Create your views here.


from django.views import View

from apps.users.models import User
from django.http import JsonResponse


class UsernameCountView(View):
    # usernames/<username>/count
    def get(self, request, username, count):
        count = User.objects.filter(username=username).count()
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
        print("这是用户名", username)
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

        return JsonResponse({'code': 0, 'errmsg': 'ok'})
