from django.contrib import admin
from .models import Building, Room, Location

# Register your models here.
admin.site.register(Building)
admin.site.register(Room)
admin.site.register(Location)
