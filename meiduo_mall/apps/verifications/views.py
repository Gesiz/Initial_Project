from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

from django.views import View


class ImageCodeView(View):
    def get(self, request, uuid):
        """
        1 接受请求
        2 提取参数
        3 验证参数
        4 生成图片验证码图片和获取验证码内容
        5 保存图片验证码
        6 返回图片响应
        :param request: 请求对象
        :param uuid:   请求参数
        :return:
        """
        # 1 接受请求
        # 2 提取参数
        # 3 验证参数
        # 4 生成图片验证码图片和获取验证码内容
        from libs.captcha.captcha import captcha
        # 返回第一个数据是 图片验证码的内容
        # 返回第二个数据是 图片验证码的图片二进制
        text, image = captcha.generate_captcha()
        # 5 保存图片验证码

        # 5.1 先链接 redis
        from django_redis import get_redis_connection
        # get_redis_connection(配置中caches名字)
        redis_cli = get_redis_connection('code')
        redis_cli.setex(uuid, 300, text)

        # 6 返回图片响应

        # 注意 我们返回的不是JSON 而是图片二进制

        return HttpResponse(image,content_type='image/jpeg')
