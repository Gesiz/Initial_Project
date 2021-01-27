from rest_framework.mixins import ListModelMixin
from rest_framework.generics import ListAPIView

from apps.users.models import User

from apps.meiduo_admin.serializers.user import UserModelSerializer
from apps.meiduo_admin.utils import PageNum

from rest_framework.generics import CreateAPIView
from rest_framework.generics import ListCreateAPIView


class UserListAPIView(ListCreateAPIView):

    def get_queryset(self):
        keyword = self.request.query_params.get('keyword')
        # 如果keyword有值 则进行模糊查询
        if keyword:
            return User.objects.filter(username__contains=keyword)
        else:
            return User.objects.all()

    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    pagination_class = PageNum
