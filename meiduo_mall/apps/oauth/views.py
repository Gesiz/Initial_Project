import json

from QQLoginTool.QQtool import OAuthQQ
from django.shortcuts import render

# Create your views here.
from django.views import View
from django.http import JsonResponse
from apps.oauth.utils import generic_openid,check_token

class QQUserView(View):
    def get(self, request):
        # 1 获取code
        code = request.GET.get('code')
        if code is None:
            return JsonResponse({'code': 400, 'errmsg': '没有code参数'})

        # 2 通过code 获取 access token
        # client_id = None,
        # client_secret = None,
        # redirect_uri = None,

        # QQ登录参数
        # 我们申请的 客户端id
        QQ_CLIENT_ID = '101474184'
        # 我们申请的 客户端秘钥
        QQ_CLIENT_SECRET = 'c6ce949e04e12ecc909ae6a8b09b637c'
        # 我们申请时添加的: 登录成功后回调的路径
        QQ_REDIRECT_URI = 'http://www.meiduo.site:8080/oauth_callback.html'

        qq = OAuthQQ(client_id=QQ_CLIENT_ID,
                     client_secret=QQ_CLIENT_SECRET,
                     redirect_uri=QQ_REDIRECT_URI)

        access_token = qq.get_access_token(code)

        openid = qq.get_open_id(access_token)
        # print(openid)

        from apps.oauth.models import OAuthQQUser
        try:
            qquser = OAuthQQUser.objects.get(openid=openid)
        except Exception as e:
            # code 必须是 300 才会显示页面  重定向

            return JsonResponse({'code': 300, 'access_token': generic_openid(openid)})
        else:
            # 如果存在 在此进行自动登录 状态保持操作
            from django.contrib.auth import login
            # login 的第二个参数 时User的实例对象
            login(request, qquser.user)
            response = JsonResponse({'code': 0, 'errmsg': 'ok'})
            response.set_cookie('username', qquser.user.username, max_age=14 * 24 * 3600)
            return response

    def post(self, request):
        # 1 接收参数
        data = json.loads(request.body.decode())
        # 2 提取参数
        mobile = data.get('mobile')
        password = data.get('password')
        sms_code = data.get('sms_code')
        access_token = data.get('access_token')
        openid = check_token(access_token)
        # 3 验证参数
        # 4 根据手机号判断用户信息
        from apps.users.models import User
        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            user = User.objects.create_user(
                username=mobile,
                mobile=mobile,
                password=password,
            )
        else:
            if not user.check_password(password):
                return JsonResponse({'code': 400, 'errmsg': '绑定失败'})
        #  若没有查询到 则新增一个用户
        #  如果查询到 则验证密码是否正确
        #
        # 5 绑定用户信息
        from apps.oauth.models import OAuthQQUser
        OAuthQQUser.objects.create(openid=openid, user=user)

        from django.contrib.auth import login
        login(request, user)

        response = JsonResponse({'code': 0, 'errmsg': 'ok'})
        response.set_cookie('username', user.username, max_age=15 * 24 * 3600)

        return response
