from django.shortcuts import render
from .forms import RouteForm
from .utils.tramviz import show_shortest, list_names
# Create your views here.


def tram_net(request):
    return render(request, 'tram/home.html', {'page_header': 'Home'})


def find_route(request):
    form = RouteForm()
    if request.method == "POST":
        form = RouteForm(request.POST)
        if form.is_valid():
            route = form.data
            timepath, geopath = show_shortest(route['dep'], route['dest'])
            timepath = list_names(timepath)
            geopath = list_names(geopath)
            return render(request, 'tram/show_route.html',
                {'dest': form.instance.__str__(), 'timepath': timepath, 'geopath': geopath})
    return render(request, 'tram/find_route.html', {'form': form})