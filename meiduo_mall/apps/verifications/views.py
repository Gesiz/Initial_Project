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

        return HttpResponse(image, content_type='image/jpeg')


######################短信验证码类视图###################
from django.http import JsonResponse
from django.http import HttpResponseBadRequest

class SmsCodeView(View):
    def get(self, request, mobile):
        """
        1 接收参数
        2 获取参数
        3 验证参数
        4 提取redis中的图片验证码
        5 把redis中的图片验证码删除
        6 用户的图片验证码和redis进行对比
        7 通过程序生成短信验证码
        8 将短信验证码保存到redis中
        9 通过云平台发送短信
        10 返回相应
        :param request:
        :param mobile:
        :return:
        """
        # 1 接收参数(手机号 用户的图片验证码 uuid)
        # /sms_codes/<mobile>/?image_code=xxxx&image_code_id=xxx
        # 2 获取参数
        # request.GET
        image_code = request.GET.get('image_code')
        uuid = request.GET.get('image_code_id')

        # 3 验证参数

        # 4 提取redis中的图片验证码

        from django_redis import get_redis_connection
        redis_cli = get_redis_connection('code')
        redis_text = redis_cli.get(uuid)

        # 5 把redis中的图片验证码删除
        redis_cli.delete(uuid)
        # 6 用户的图片验证码和redis进行对比

        if image_code.lower() != redis_text.decode().lower():
            print("验证码错误")

            return JsonResponse({'code': 400, 'errmsg': '图片验证码错误'})

        # 再说生成短信验证码前 判断标记
        send_flag = redis_cli.get(f'send_flag_{mobile}')

        if send_flag is not None:
            return HttpResponseBadRequest("不要重复操作")
            # return JsonResponse({'status_code': 400, 'errmsg': '存在频繁操作'})

        # 7 通过程序生成短信验证码
        from random import randint
        sms_code = randint(100000, 999999)

        # 8 将短信验证码保存到redis中
        # 创建管道 通过 redis 的客户端 创建一个 管道 pipeline
        pipeline = redis_cli.pipeline()

        pipeline.setex(mobile, 600, sms_code)
        pipeline.setex(f'send_flag_{mobile}', 60, 1)
        pipeline.execute()

        # 10 分钟过期 600s

        # redis_cli.setex(mobile, 600, sms_code)
        #
        # redis_cli.setex(f'send_flag_{mobile}', 60, 1)
        # 9 通过云平台发送短信
        from celery_tasks.sms.tasks import celery_send_sms_code
        celery_send_sms_code.delay(mobile, sms_code)
        # from ronglian_sms_sdk import SmsSDK
        # accId = '8aaf0708762cb1cf0176c60392973587'
        # accToken = 'a099e3b6a8a14e09bae6d133051decb9'
        # appId = '8aaf0708762cb1cf0176c603936b358e'
        # sdk = SmsSDK(accId, accToken, appId)
        # tid = '1'  # 因为是测试用户 所以我们发送短信的模板只能是1
        # mobile = f'{mobile}'
        # datas = (sms_code, 7777)  # 涉及到模板的变量
        # # 您的验证码为 1 请于 2 分钟内输入
        # resp = sdk.sendMessage(tid, mobile, datas)
        # print(resp)
        return JsonResponse({'code': 0, 'errmsg': '验证码发送成功'})
