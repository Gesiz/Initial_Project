from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from apps.meiduo_admin.views import home
from .login import admin_obtain_token
from apps.meiduo_admin.views import user
urlpatterns = [
    path('authorizations/', admin_obtain_token),
    path('statistical/day_active/', home.UserActiveAPIView.as_view()),
    path('statistical/day_orders/', home.UserOrderAPIView.as_view()),
    path('statistical/month_increment/', home.MonthUserAPIView.as_view()),
    path('users/', user.UserListAPIView.as_view()),
]
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('skus/images')