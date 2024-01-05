from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from buildings.models import Building, Room, Location


class BuildingViewsTest(APITestCase):

    def _create_mock_data(self):
        location_a = Location.objects.create(name='Location A')
        location_b = Location.objects.create(name='Location B')
        building_a = Building.objects.create(
            name='Building A',
            year=Building.YearInSchool.FRESHMAN,
            location=location_a,
            laundry_floors='1',
            capacity=100,
            address='123 Maple St.',
            is_gph=False,
        )
        building_b = Building.objects.create(
            name='Building B',
            year=Building.YearInSchool.SOPHOMORE,
            location=location_a,
            laundry_floors='1',
            capacity=100,
            address='123 Main St.',
            is_gph=False,
        )
        building_c = Building.objects.create(
            name='Building C',
            year=Building.YearInSchool.ANY,
            location=location_b,
            laundry_floors='1,3',
            capacity=100,
            address='500 Hope St.',
            is_gph=True,
        )
        Room.objects.create(
            room_name='Building A Room A',
            floor=3,
            floor_plan_url='',
            number=0,
            sqft=50,
            capacity=2,
            building=building_a,
            is_suite=False,
        )
        Room.objects.create(
            room_name='Building A Room B',
            floor=2,
            floor_plan_url='',
            number=1,
            sqft=75,
            capacity=3,
            building=building_a,
            is_suite=True,
        )
        Room.objects.create(
            room_name='Building B Room A',
            floor=1,
            floor_plan_url='',
            number=0,
            sqft=50,
            capacity=2,
            building=building_b,
            is_suite=False,
        )
        Room.objects.create(
            room_name='Building B Room B',
            floor=2,
            floor_plan_url='',
            number=1,
            sqft=25,
            capacity=1,
            building=building_b,
            is_suite=True,
        )
        Room.objects.create(
            room_name='Building C Room A',
            floor=1,
            floor_plan_url='',
            number=0,
            sqft=50,
            capacity=2,
            building=building_c,
            is_suite=False,
        )

    def setUp(self):
        """
        Called before each individual test.
        """
        self._create_mock_data()

    def test_get_all_buildings(self):
        url = reverse("list_buildings")
        response = self.client.get(url)
        building_count = Building.objects.all().count()
        self.assertEqual(len(response.data), building_count)
        print(response.data[0])

    def test_get_all_rooms(self):
        url = reverse("list_rooms")
        response = self.client.get(url)
        room_count = Room.objects.all().count()
        self.assertEqual(len(response.data), room_count)

