from django.db import models


class Area(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    longitude = models.FloatField()
    latitude = models.FloatField()

    def number_of_locations(self):
        """
        Returns the number of locations for this area.
        :return: num_locations
        """
        return self

    def average_measurement(self):
        """
        Returns the average of the measurements for this area.
        If the area has no measurements then return None.
        :return: average
        """
        return self

    def category_names(self):
        """
        Returns a string with a list of categories that this area belongs to.
        The names should be comma separated.
        If the area belongs to no categories, return the empty string.
        :return: names
        """
        return self

    def __str__(self):
        return self.name


class Location(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    altitude = models.IntegerField()
    area = models.ForeignKey(Area)

    # Area:Location
    def __str__(self):
        return self.name


class Measurement(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.FloatField()
    date = models.DateTimeField()
    location = models.ForeignKey(Location)

    # Measurement@Area:Location
    def __str__(self):
        return self.name


class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    members = models.ManyToManyField(Area)

    # Measurement@Area:Location
    def __str__(self):
        return self.name
