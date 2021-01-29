from rest_framework import serializers

from apps.orders.models import OrderInfo, OrderGoods
from apps.goods.models import SKU


class OrdersInfoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderInfo
        fields = ['order_id', 'create_time']


class OrderSKUModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SKU
        fields = ['name', 'default_image']


class OrderSKUSModelSerializer(serializers.ModelSerializer):
    sku = OrderSKUModelSerializer()

    class Meta:
        model = OrderGoods
        fields = ['count', 'price', 'sku']


# 订单详情外层序列化器
class OrdersDetailModelSerializer(serializers.ModelSerializer):
    skus = OrderSKUSModelSerializer(many=True)

    class Meta:
        model = OrderInfo
        fields = ['order_id', 'user', 'total_count', "order_id", "user",
                  "total_count", "total_amount", "freight", "pay_method", "status",
                  "create_time", "skus"]


class OrderUpdateModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderInfo
        fields = ['order_id', 'status']

    # def update(self, instance, validated_data):
    #     super().update(instance,**validated_data)
    #     print(validated_data)
    #     return  instance
