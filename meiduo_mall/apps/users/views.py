from django.shortcuts import render

# Create your views here.


from django.views import View

from apps.users.models import User
from django.http import JsonResponse


class UsernameCountView(View):
    # usernames/<username>/count
    def get(self, request, username, count):
        count = User.objects.filter(username=username).count()
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'count': count})


class RegisterView(View):

    def post(self, request):
        pass
