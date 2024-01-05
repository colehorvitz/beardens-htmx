# JSON parser to populate preexisting RDF data into Django models

import json
import sys
import django
import os
import subprocess

BUILDING_JSON_PATH = "data/json/BuildingData.json"
ROOM_JSON_PATH	= "data/json/RoomData.json"
MEDIA_PATH = "media/"

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "beardens.settings")
django.setup()

from buildings.models import Building, Room, Location

def parse_buildings():
	with open(BUILDING_JSON_PATH) as f:
		raw = json.load(f)
		data = raw['results']['bindings']
		for building in data:
			
			building_name = building['buildingLabel']['value']
			class_year_raw = building['buildingClassYearLabel']['value']
			class_year = Building.YearInSchool.FRESHMAN if class_year_raw == "Freshmen" else Building.YearInSchool.SOPHOMORE if class_year_raw == "Sophomores" else Building.YearInSchool.ANY if class_year_raw == "Any" else Building.YearInSchool.JUNIOR_SENIOR 
			laundry_floors = building['laundryFloorLabels']['value'].replace(" and ", ",")
			capacity = building['buildingCapacity']['value']
			location = building['buildingLocationLabel']['value']
			address = building['buildingAddress']['value']
			image_url = building['imageURL']['value']
			is_gph = True if building['isGPH']['value'] == "Yes" else False
			location, created = Location.objects.get_or_create(name=location)
			if created:
				print("Creating Location model for {}".format(building_name))
	
			if Building.objects.filter(name=building_name).exists():
				print("ERROR: Building already exists with name {}".format(building_name))
			else:
				building = Building.objects.create(name=building_name, year=class_year, laundry_floors=laundry_floors, capacity=capacity, address=address, is_gph=is_gph, location=location)	
				print("Created model {}".format(building))


def parse_rooms():
	with open(ROOM_JSON_PATH) as f:
		raw = json.load(f)
		data = raw['results']['bindings']
		for room in data:
			building_name = room['buildingLabel']['value']
			try:
				building = Building.objects.get(name=building_name)
			except Building.DoesNotExist:
				print("Unable to find building {}, continuing".format(building_name))
				continue
			room_label = room['roomLabel']['value']
			room_number = room['roomNumber']['value']
			floor_level = room['floorLabel']['value']
			floor_plan_url = room['floorPlanURI']['value']
			is_suite = True if room['isSuite']['value'] == "Yes" else False
			sqft = room['sqft']['value']
			num_occupants_raw = room['numOccupants']['value']
			num_occupants = Room.RoomSize.SINGLE if num_occupants_raw == "Single" else Room.RoomSize.DOUBLE if num_occupants_raw == "Double" else Room.RoomSize.TRIPLE if num_occupants_raw == "Triple" else Room.RoomSize.QUAD
			if Room.objects.filter(room_name=room_label, number=room_number, building=building, is_suite=is_suite, sqft = sqft, capacity=num_occupants, floor=floor_level, floor_plan_url=floor_plan_url).exists():
				continue
			room = Room.objects.create(room_name=room_label, floor=floor_level, floor_plan_url=floor_plan_url, number=room_number, sqft=sqft, capacity=num_occupants, building=building, is_suite=is_suite)
			print("Created room {}".format(room))


def set_thumbnails():
	with open(BUILDING_JSON_PATH) as f:
		raw = json.load(f)
		data = raw['results']['bindings']
		for building in data:
			img_url = building['imageURL']['value']
			name = building['buildingLabel']['value']
			file_name =  '{}.jpg'.format(name.replace(' ', ''))
			file_path = MEDIA_PATH + file_name
			if not os.path.isfile(file_path):
				subprocess.run(['wget', img_url, '-O', file_path])
			building = Building.objects.filter(name=name)
			if building.exists():
				building = building.first()
				if building.image == file_name:
					continue		
				building.image = file_name
				building.save()
				print("Set {} thumbnail to {}".format(name, file_path))


def parse():
	parse_buildings()
	set_thumbnails()
	parse_rooms()

def delete_all_rooms():
	Room.objects.all().delete()

def main():
	parse()
	
if __name__ == "__main__":
	main()
