from apps.goods.models import SKU, SPU, SKUSpecification
from rest_framework import serializers


class SKUSpecificationModelSerializer(serializers.ModelSerializer):
    spec_id = serializers.IntegerField()
    option_id = serializers.IntegerField()

    class Meta:
        model = SKUSpecification
        fields = ['spec_id', 'option_id']


class SKUModelSerializer(serializers.ModelSerializer):
    # category_id 对应外键值
    category_id = serializers.IntegerField()
    # category 对应的模型 __str__ 返回的数据
    category = serializers.StringRelatedField

    spu_id = serializers.IntegerField()
    spu = serializers.StringRelatedField()
    specs = SKUSpecificationModelSerializer(many=True)

    class Meta:
        model = SKU
        fields = '__all__'

    def create(self, validated_data):
        # 1 把 1 对多的 的数据pop出来
        specs = validated_data.pop('specs')

        from django.db import transaction

        with transaction.atomic():
            save_point = transaction.savepoint()
            try:
                # 2 validated_data 就剩下sku 数据
                sku = SKU.objects.create(**validated_data)
                # 对多的数据进行遍历
                for spec in specs:
                    SKUSpecification.objects.create(sku=sku, **spec)
            except Exception:
                transaction.savepoint_rollback(save_point)
            else:
                transaction.savepoint_commit(save_point)
        return sku

    def update(self, instance, validated_data):
        specs = validated_data.pop('specs')
        super().update(instance, validated_data)
        for spec in specs:
            SKUSpecification.objects.filter(
                sku=instance,
                spec_id=spec.get('spec_id'),
            ).update(
                option_id=spec.get('option_id')
            )
        return instance


from apps.goods.models import GoodsCategory


class GoodsCategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = ['id', 'name']


#################SPU############
class SimpleSPUModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SPU
        fields = ['id', 'name']


from apps.goods.models import SpecificationOption


class SpecificationOptionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecificationOption
        fields = "__all__"


from apps.goods.models import SPUSpecification


class SPUSpecModelSerializer(serializers.ModelSerializer):
    spu = serializers.StringRelatedField()
    spu_id = serializers.IntegerField()

    options = SpecificationOptionModelSerializer(many=True)

    class Meta:
        model = SPUSpecification
        fields = ['id', 'name', 'spu', 'spu_id', 'options']
