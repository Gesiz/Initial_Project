from django.urls import path
from apps.users.views import UsernameCountView, RegisterView, MobileCountView, \
    LoginView, LogoutView,UserInfoVIew,EmailView

urlpatterns = [
    path('usernames/<uc:username>/count/', UsernameCountView.as_view()),
    path('mobiles/<mc:mobile>/count/', MobileCountView.as_view()),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('info/',UserInfoVIew.as_view()),
    path('emails/',EmailView.as_view()),
]
