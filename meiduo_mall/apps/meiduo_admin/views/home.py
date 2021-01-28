from datetime import date
from apps.users.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone


class UserActiveAPIView(APIView):
    def get(self, request):
        today = date.today()
        count = User.objects.filter(last_login__gte=today).count()
        return Response({'count': count})


class UserOrderAPIView(APIView):
    def get(self, request):
        today = date.today()
        count = User.objects.filter(orderinfo__create_time__gte=today).count()
        return Response({'count': count})


class UserTotalAPIView(APIView):
    def get(self, request):
        today = date.today()
        count = User.objects.all().count()
        return Response({
            "count": count,
            "date": today
        })


from datetime import timedelta


class MonthUserAPIView(APIView):
    def get(self, request):
        today = date.today()
        before_date = today - timedelta(days=30)
        # 初始化一个列表
        data_list = []
        for i in range(0, 30):
            start_date = before_date + timedelta(days=i)
            end_date = before_date + timedelta(days=(i + 1))
            count = User.objects.filter(date_joined__gte=start_date, date_joined__lt=end_date).count()
            data_list.append(
                {
                    'count': count,
                    'date': start_date
                }
            )

        return Response(data_list)
