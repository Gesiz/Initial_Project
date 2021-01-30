from django.contrib.auth.models import Permission
from rest_framework import serializers


class PermissionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'


from django.contrib.auth.models import ContentType


class ContentTypeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentType
        fields = ['id', 'name']
