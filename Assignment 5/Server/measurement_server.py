from http.server import HTTPServer, BaseHTTPRequestHandler
import sqlite3
import json
import re
import collections

# =====================================================================================================================
# Course:       Internet Programming
# Instructor:   Ben Setzer
# Assignment:   #5
# Author:       Dhruval Darji
__author__ = 'Dhruval Darji'


# =====================================================================================================================
# =====================================================================================================================
# Overview:
# This script will respond to requests for data from the measurement
# database by sending back data that is JSON serialized.
# The server should listen on any interface at port 12345.
# =====================================================================================================================
# =====================================================================================================================
# Path                            | Function                                              | Return Type
# =====================================================================================================================
# /area	                          | Get a list of all areas                               | Dictionary (JSON)
# /area/(\d+)/location	          | Get all locations for the given area id               | Dictionary (JSON)
# /location/(\d+)/measurement	  | Get all the measurements for the given location id    | Dictionary (JSON)
# /area/(\d+)/category	          | Get all the categories to which the given area belongs| Dictionary (JSON)
# /area/(\d+)/average_measurement | Get the average measurement for the given area        | Number (JSON)
# /area/(\d+)/number_locations	  | Get the number of locations in the given area         | Number (JSON)
# =====================================================================================================================

host = '0.0.0.0'
port = 12345

# Define Regex for URLs
re_areas = re.compile('/area')
re_locations = re.compile('/area/(\d+)/location')
re_measurements = re.compile('/location/(\d+)/measurement')
re_categories = re.compile('/area/(\d+)/category')
re_averages = re.compile('/area/(\d+)/average_measurement')
re_totals = re.compile('/area/(\d+)/number_locations')

re_favicon = re.compile('/favicon.ico')


# ==========================================================================================================


# Return Areas as a JSON Dictionary.
def get_areas():
    conn = sqlite3.connect('measures.sqlite')

    # create a cursor to navigate this database
    c = conn.cursor()

    # Execute an SQL statement; results are stored in the cursor
    c.execute('SELECT * FROM area')
    rows = c.fetchall()

    # Convert query JSON
    # Convert query to objects of key-value pairs
    objects_list = []
    for row in rows:
        d = collections.OrderedDict()
        d['id'] = row[0]
        d['name'] = row[1]
        d['longitude'] = row[2]
        d['latitude'] = row[3]
        objects_list.append(d)

    j = json.dumps(objects_list)
    conn.close()

    return j


# Return Locations as a JSON Dictionary.
def get_locations(area_id):
    conn = sqlite3.connect('measures.sqlite')

    # create a cursor to navigate this database
    c = conn.cursor()

    # Execute an SQL statement; results are stored in the cursor
    c.execute('SELECT * FROM location WHERE location_area =' + area_id)
    rows = c.fetchall()

    # Convert query JSON
    # Convert query to objects of key-value pairs
    objects_list = []
    for row in rows:
        d = collections.OrderedDict()
        d['id'] = row[0]
        d['area'] = row[1]
        d['name'] = row[2]
        d['altitude'] = row[3]
        objects_list.append(d)

    j = json.dumps(objects_list)
    conn.close()

    return j


# Return Measurements as a JSON Dictionary.
def get_measurements(location_id):
    conn = sqlite3.connect('measures.sqlite')

    # create a cursor to navigate this database
    c = conn.cursor()

    # Execute an SQL statement; results are stored in the cursor
    c.execute('SELECT * FROM measurement WHERE measurement_location = ' + location_id)
    rows = c.fetchall()

    # Convert query JSON
    # Convert query to objects of key-value pairs
    objects_list = []
    for row in rows:
        d = collections.OrderedDict()
        d['id'] = row[0]
        d['value'] = row[1]
        d['location'] = row[2]
        objects_list.append(d)

    j = json.dumps(objects_list)
    conn.close()

    return j


# Return Categories as a JSON Dictionary.
def get_categories(area_id):
    conn = sqlite3.connect('measures.sqlite')

    # create a cursor to navigate this database
    c = conn.cursor()

    # Execute an SQL statement; results are stored in the cursor
    c.execute('SELECT * FROM category_area '
              'INNER JOIN category on category.category_id = category_area.category_id '
              'INNER JOIN area ON area.area_id = category_area.area_id '
              'WHERE area.area_id = ' + area_id + ';')

    rows = c.fetchall()

    # Convert query JSON
    # Convert query to objects of key-value pairs
    objects_list = []
    for row in rows:
        d = collections.OrderedDict()
        d['category_id'] = row[0]
        d['area_id'] = row[1]

        # d['id'] = row[0]
        # d['name'] = row[1]
        # d['description'] = row[2]
        objects_list.append(d)

    j = json.dumps(objects_list)
    conn.close()

    return j


# Return the average measurements for a given area as a JSON Number.
def get_avg_measurement(area_id):
    conn = sqlite3.connect('measures.sqlite')

    # create a cursor to navigate this database
    c = conn.cursor()
    # Execute an SQL statement; results are stored in the cursor
    c.execute('SELECT AVG(value) FROM measurement '
              'INNER JOIN location on location.location_id = measurement.measurement_location '
              'INNER JOIN area ON area.area_id = location.location_area '
              'WHERE area.area_id = ' + area_id + ';')
    average = c.fetchone()[0]

    # Convert query JSON Number

    j = json.dumps(average)
    conn.close()

    return j


# Return the total number of locations for a given area as a JSON Number.
def get_total_locations(area_id):
    conn = sqlite3.connect('measures.sqlite')

    # create a cursor to navigate this database
    c = conn.cursor()

    # Execute an SQL statement; results are stored in the cursor
    c.execute('SELECT COUNT(*) FROM location '
              'INNER JOIN area ON area.area_id = location.location_area '
              'WHERE area.area_id = ' + area_id + ';')
    total = c.fetchone()[0]

    # Convert query JSON

    j = json.dumps(total)
    conn.close()

    return j

# ==========================================================================================================


class MyRestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if re.search(re_areas, self.path) and len(self.path) == 5:
            areas = get_areas()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            data = areas.encode()
            self.wfile.write(data)

        if re.search(re_locations, self.path):
            area_id = self.path.split('/')[2]
            locations = get_locations(area_id)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            data = locations.encode()
            self.wfile.write(data)

        if re.search(re_measurements, self.path):
            location_id = self.path.split('/')[2]
            measurements = get_measurements(location_id)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            data = measurements.encode()
            self.wfile.write(data)

        if re.search(re_categories, self.path):
            area_id = self.path.split('/')[2]
            categories = get_categories(area_id)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            data = categories.encode()
            self.wfile.write(data)

        if re.search(re_averages, self.path):
            area_id = self.path.split('/')[2]
            average = get_avg_measurement(area_id)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            data = average.encode()
            self.wfile.write(data)

        if re.search(re_totals, self.path):
            area_id = self.path.split('/')[2]
            total = get_total_locations(area_id)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            data = total.encode()
            self.wfile.write(data)

        if re.search(re_favicon, self.path):
            fav = open('/favicon.png')
            self.send_response(200)
            self.send_header('Content-Type', 'image/png')
            self.end_headers()
            self.wfile.write(fav.read())


server = HTTPServer((host, port), MyRestHandler)

server.serve_forever()