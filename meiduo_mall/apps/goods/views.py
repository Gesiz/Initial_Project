from django.shortcuts import render
from django.views import View
from utils.goods import *


# Create your views here.
class IndexView(View):
    def get(self, request):
        categories = get_categories()

        contents = get_contents()

        context = {
            'categories': categories,
            'contexts': contents
        }
        return render(request, 'index.html', context=context)
