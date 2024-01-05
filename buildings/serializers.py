from rest_framework import serializers
from .models import Building, Room


class RoomSerializer(serializers.ModelSerializer):
    capacity_label = serializers.CharField(
        source='get_capacity_display', read_only=True)

    class Meta:
        model = Room
        fields = (
            'pk',
            'name',
            'floor',
            'room_number',
            'sqft',
            'capacity_label',
            'floor_plan_url',
            'is_suite',
        )


class BuildingSerializer(serializers.ModelSerializer):
    class_year_label = serializers.CharField(source="get_year_display")
    location = serializers.CharField(source='location.name')
    rooms = RoomSerializer(many=True, read_only=True)

    class Meta:
        model = Building
        fields = (
            'pk',
            'name',
            'class_year_label',
            'laundry_floors',
            'capacity',
            'location',
            'address',
            'is_gph',
            'image',
            'room_count',
            'rooms',
        )
