from django.urls import path

from . import views

urlpatterns = [
    path('index/', views.IndexView.as_view()),
    path('list/<category_id>/skus/', views.ListView.as_view()),
    path('hot/<category_id>/', views.HotView.as_view()),
    path('detail/<sku_id>/', views.DetailView.as_view()),
]
