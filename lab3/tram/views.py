from django.shortcuts import render
from .models import Fruit
# Create your views here.


def post_list(request):
    image = '../../static/mygraph.svg'
    return render(request, 'tram/post_list.html', {'image': image})
