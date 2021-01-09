from django.urls import path
from apps.users.views import UsernameCountView, RegisterView, MobileCountView, \
    LoginView, LogoutView, UserInfoVIew, EmailView, VerifyEmailView, \
    CreateAddressView, AddressesListView, UserHistoryView

urlpatterns = [
    path('usernames/<uc:username>/count/', UsernameCountView.as_view()),
    path('mobiles/<mc:mobile>/count/', MobileCountView.as_view()),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('info/', UserInfoVIew.as_view()),
    path('emails/', EmailView.as_view()),
    path('emails/verification/', VerifyEmailView.as_view()),
    path('addresses/create/', CreateAddressView.as_view()),
    path('addresses/', AddressesListView.as_view()),
    path('browse_histories/', UserHistoryView.as_view()),

]
