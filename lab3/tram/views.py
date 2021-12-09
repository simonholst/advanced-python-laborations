from django.shortcuts import render
from .forms import RouteForm
# Create your views here.


def tram_net(request):
    return render(request, 'tram/home.html', {})


def find_route(request):
    form = RouteForm()
    return render(request, 'tram/find_route.html', {'form': form})