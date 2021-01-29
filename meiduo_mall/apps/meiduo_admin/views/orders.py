from rest_framework.views import APIView
from apps.meiduo_admin.serializers.orders import OrdersInfoModelSerializer, OrdersDetailModelSerializer, \
    OrderUpdateModelSerializer
from apps.meiduo_admin.utils import PageNum
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView
from apps.orders.models import OrderInfo, OrderGoods
from rest_framework.response import Response


class OrdersInfoAPIView(ListAPIView):
    serializer_class = OrdersInfoModelSerializer
    pagination_class = PageNum

    def get_queryset(self):
        keyword = self.request.query_params.get('keyword')

        if keyword == '' or keyword is None:
            return OrderInfo.objects.all().order_by('order_id')
        else:
            return OrderInfo.objects.filter(order_id__contains=keyword).order_by('order_id')


class OrdersDetailAPIView(RetrieveAPIView):
    serializer_class = OrdersDetailModelSerializer
    queryset = OrderInfo.objects.all()


class UpdateStatusAPIView(UpdateAPIView):
    serializer_class = OrderUpdateModelSerializer
    queryset = OrderInfo.objects.all()
    lookup_field = 'order_id'

    def update(self, request, *args, **kwargs):
        try:
            order = OrderInfo.objects.get(**kwargs)
            order.status = request.data.get('status')
            order.save()
        except Exception:
            pass
        else:
            return Response({
                'order_id': order.order_id,
                'status': order.status
            }, status=201)
