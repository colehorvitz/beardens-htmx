from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_comma_separated_integer_list

# Create your models here.


class Location(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Building(models.Model):
    class YearInSchool(models.TextChoices):
        FRESHMAN = "FR", _("Freshman")
        SOPHOMORE = "SO", _("Sophomore")
        JUNIOR_SENIOR = "JRSR", _("Junior/Senior")
        ANY = "ANY", _("Any")

    name = models.CharField(max_length=255)
    year = models.CharField(
        max_length=24, choices=YearInSchool.choices, default=YearInSchool.ANY
    )
    laundry_floors = models.CharField(
        validators=[validate_comma_separated_integer_list], max_length=24, default=""
    )
    capacity = models.PositiveSmallIntegerField()
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name="buildings"
    )
    address = models.CharField(max_length=255)
    is_gph = models.BooleanField(default=False)
    image = models.ImageField(blank=True)

    @property
    def room_count(self):
        return self.rooms.all().count()

    def __str__(self):
        return self.name


class Room(models.Model):
    class RoomSize(models.TextChoices):
        SINGLE = "SI", _("Single")
        DOUBLE = "DO", _("Double")
        TRIPLE = "TR", _("Triple")
        QUAD = "QU", _("Quad")

    name = models.CharField(max_length=255)
    floor = models.PositiveSmallIntegerField()
    room_number = models.CharField(max_length=5)
    sqft = models.IntegerField()
    capacity = models.CharField(choices=RoomSize.choices, max_length=24)
    building = models.ForeignKey(
        Building, on_delete=models.CASCADE, related_name="rooms"
    )
    floor_plan_url = models.URLField()
    is_suite = models.BooleanField(default=False)

    def __str__(self):
        return "{} {}".format(self.building, self.room_number)
