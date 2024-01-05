from django.shortcuts import render
from .models import Building, Room
from django.shortcuts import get_object_or_404


def index(request):
    buildings = Building.objects.all()
    return render(
        request,
        "buildings/index.html",
        {"buildings": buildings, "selected_building": buildings.first()},
    )


def building_detail(request, pk):
    buildings = Building.objects.all()
    building = get_object_or_404(Building, pk=pk)
    return render(
        request,
        "buildings/display.html",
        {"buildings": buildings, "selected_building": building},
    )
