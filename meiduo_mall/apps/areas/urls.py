from django.urls import path
# from apps.areas.views import ProvinceView
from . import views

urlpatterns = [
    path('areas/', views.ProvinceView.as_view()),
    path('areas/<pk>/', views.SubAreaView.as_view()),
    path('addresses/<address_id>/', views.UpdateDestroyAddressView.as_view()),
    path('addresses/<address_id>/default/', views.DefaultAddressView.as_view()),
    path('addresses/<address_id>/title/', views.UpdateTitleAddressView.as_view()),
    path('password/', views.UpdateTitleAddressView.as_view()),

]
