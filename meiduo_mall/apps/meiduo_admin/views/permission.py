"""
所谓的权限还是会体现在模型的增删改查
"""

from rest_framework.viewsets import ModelViewSet

from django.contrib.auth.models import Permission
from django.contrib.auth.models import ContentType
from apps.meiduo_admin.serializers.permission import PermissionModelSerializer,ContentTypeModelSerializer
from apps.meiduo_admin.utils import PageNum


class PermissionModelViewSet(ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionModelSerializer
    pagination_class = PageNum



from django.contrib.auth.models import ContentType

from rest_framework.generics import ListAPIView

class ContentTypeListAPIView(ListAPIView):
    queryset = ContentType.objects.all()
    serializer_class = ContentTypeModelSerializer