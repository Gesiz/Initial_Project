from django.urls import path
# from apps.areas.views import ProvinceView
from . import views

urlpatterns = [
    path('areas/', views.ProvinceView.as_view()),
    path('areas/<pk>/', views.SubAreaView.as_view()),
]
