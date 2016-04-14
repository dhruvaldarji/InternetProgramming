from django.db import models, connection


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
        c = connection.cursor()
        c.execute('SELECT COUNT(*) FROM measurements_location WHERE area_id = %s;', [self.id])
        num_locations = c.fetchone()[0]

        return num_locations

    def average_measurement(self):
        """
        Returns the average of the measurements for this area.
        If the area has no measurements then return None.
        :return: average
        """
        c = connection.cursor()
        c.execute('SELECT ROUND(AVG(value), 3) FROM measurements_measurement ' +
                  'INNER JOIN measurements_location ON measurements_location.id = measurements_measurement.location_id ' +
                  'INNER JOIN measurements_area ON measurements_area.id = measurements_location.area_id ' +
                  'WHERE measurements_area.id = %s;', [self.id])
        average = c.fetchone()[0]

        return average

    def category_names(self):
        """
        Returns a string with a list of categories that this area belongs to.
        The names should be comma separated.
        If the area belongs to no categories, return the empty string.
        :return: names
        """
        cats = ""
        c = connection.cursor()
        c.execute('SELECT * FROM measurements_category ' +
                  'INNER JOIN measurements_category_members ON measurements_category_members.category_id = measurements_category.id ' +
                  'INNER JOIN measurements_area ON measurements_area.id = measurements_category_members.area_id ' +
                  'WHERE measurements_area.id = %s;', [self.id])
        rows = c.fetchall()

        category_names = []
        for row in rows:
            category_names.append(row[1])

        cats = ', '.join(category_names)
        if cats == '':
            return 'None'
        else:
            return cats

    def __str__(self):
        return self.name


class Location(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    altitude = models.IntegerField()
    area = models.ForeignKey(Area)

    # Area:Location
    def __str__(self):
        return self.area.__str__() + ":" + self.name


class Measurement(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.FloatField()
    date = models.DateTimeField()
    location = models.ForeignKey(Location)

    # Measurement@Area:Location
    def __str__(self):
        return "Measurement@" + self.location.__str__()


class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    members = models.ManyToManyField(Area)

    # Measurement@Area:Location
    def __str__(self):
        return self.name
