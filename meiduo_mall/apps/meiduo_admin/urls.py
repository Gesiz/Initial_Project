from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from apps.meiduo_admin.views import home
from .login import admin_obtain_token
from apps.meiduo_admin.views import user, image,sku,orders

urlpatterns = [
    # 添加自定义登录系统 进行管理员登录控制 需要重写 obtain_jwt_token
    path('authorizations/', admin_obtain_token),
    # 统计当日活跃用户
    path('statistical/day_active/', home.UserActiveAPIView.as_view()),
    # 统计当日下单用户量
    path('statistical/day_orders/', home.UserOrderAPIView.as_view()),
    # 总用户量
    path('statistical/total_count/', home.UserTotalAPIView.as_view()),
    # 日增用户统计
    path('statistical/day_increment/', home.DayUserAPIView.as_view()),

    # 月增用户统计
    path('statistical/month_increment/', home.MonthUserAPIView.as_view()),


    # 订单管理
    path('orders/', orders.OrdersInfoAPIView.as_view()),
    path('orders/<pk>/', orders.OrdersDetailAPIView.as_view()),
    path('orders/<order_id>/status/', orders.UpdateStatusAPIView.as_view()),


    # 获取用户数据
    path('users/', user.UserListAPIView.as_view()),

    # 图片中获取SKU
    path('skus/simple/', image.SimpleSkuListAPIView.as_view()),

    path('skus/categories/', sku.GoodCategoryAPIView.as_view()),


    path('goods/<spu_id>/specs/', sku.GoodSpecsAPIView.as_view()),

    path('goods/simple/',sku.SPUSimpleListAPIView.as_view())
]
from rest_framework.routers import DefaultRouter
# 路由集需要使用router创建路由集
# 创建router
router = DefaultRouter()
# 注册url
router.register('skus/images', image.ImageModelViewSet, basename='images')
# 添加
# SKU展示
urlpatterns += router.urls
router.register('skus', sku.SKUModelViewSet, basename='skus')
# 添加
urlpatterns += router.urls
