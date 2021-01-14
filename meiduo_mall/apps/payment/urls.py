from django.urls import path
from . import views

urlpatterns = [
    path('payment/status/', views.PayCommitView.as_view()),
    path('payment/<order_id>/', views.PayURLView.as_view()),
]
