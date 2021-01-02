from django.urls import path
from apps.users.views import UsernameCountView

urlpatterns = [
    path('usernames/<uc:username>/<count>/', UsernameCountView.as_view())
]
