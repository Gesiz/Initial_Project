from django.urls import path
from apps.areas.views import ProvinceView

urlpatterns = [
    path('areas/', ProvinceView.as_view())
]
