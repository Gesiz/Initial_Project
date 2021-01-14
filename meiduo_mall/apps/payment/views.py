from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from utils.views import LoginRequiredJSONMixin
from apps.orders.models import OrderInfo

class PayURLView(LoginRequiredJSONMixin,View):

    def get(self,request,order_id):
        """
        0. 必须是登录用户, 获取用户信息
        1. 获取order_id
        2. 根据订单id查询订单信息
        3. 创建支付宝 支付对象
        4. 生成 order_string
        5. 拼接url
        6. 返回支付url
        :param request:
        :param order_id:
        :return:
        """
        # 0. 必须是登录用户, 获取用户信息
        user=request.user
        # 1. 获取order_id   url中有
        # 2. 根据订单id查询订单信息
        # 查询更准确,多添加一些条件
        try:
            order = OrderInfo.objects.get(order_id=order_id,user=user)
        except OrderInfo.DoesNotExist:
            return JsonResponse({'code':400,'errmsg':'没有此订单'})

        # https://github.com/fzlee/alipay/blob/master/README.zh-hans.md
        # 3. 创建支付宝 支付对象
        from alipay import AliPay
        from alipay.utils import AliPayConfig
        # 3.1 通过文件的形式 来 读取 美多私钥  和 支付宝 公钥
        # 我们最好设置一个相对路径,把相对路径的配置 放到 settings.py中
        from meiduo_mall import settings
        app_private_key_string = open(settings.APP_PRIVATE_KEY_PATH).read()
        alipay_public_key_string = open(settings.ALIPAY_PUBLIC_KEY_PATH).read()

        alipay = AliPay(
            appid=settings.ALIPAY_APPID,
            app_notify_url=None,  # 默认回调url
            app_private_key_string=app_private_key_string,
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_string=alipay_public_key_string,
            sign_type="RSA2",  # RSA 或者 RSA2
            debug = False,  # 默认False
            config = AliPayConfig(timeout=15)  # 可选, 请求超时时间
        )
        # 4. 通过电脑网址支付的方法, 来生成 order_string
        # 如果你是 Python 3的用户，使用默认的字符串即可
        subject = "测试订单"

        # 电脑网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=order_id,                               # 美多商城的订单id
            total_amount=str(order.total_amount),                # 订单总金额  类型转换为 str
            subject=subject,
            return_url=settings.ALIPAY_RETURN_URL,                   # 支付成功之后,最终要跳转会美多
            #notify_url="https://example.com/notify"  # 可选, 不填则使用默认notify url
        )
        # 5. 拼接url
        alipay_url = 'https://openapi.alipaydev.com/gateway.do?' + order_string

        # 6. 返回支付url
        return JsonResponse({'code':0,'alipay_url':alipay_url})

class PayCommitView(View):

    def put(self, request):
        """
        1. 接受参数
        2. 提取参数
        3. 保存入库
        4. 更新订单状态
        5. 返回响应
        :param request:
        :return:
        """
        # 1. 接受参数
        data = request.GET
        # 2. 提取参数
        out_trade_no = data.get('out_trade_no')  # 美多商城的订单aidi
        trade_no = data.get('trade_no')  # 支付宝交易流水号

        # 3. 保存入库
        Payment.objects.create(
            order_id=out_trade_no,
            trade_id=trade_no
        )
        # 4. 更新订单状态
        OrderInfo.objects.filter(oder_id=out_trade_no).update(status=OrderInfo.ORDER_STATUS_ENUM['UNSEND'])
        # 5. 返回响应
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'trade_id': trade_no})