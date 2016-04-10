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
# /area/(\d+)	                  | Get area by id                                        | Object (JSON)
# /area/(\d+)/location	          | Get all locations for the given area id               | Dictionary (JSON)
# /area/(\d+)/category	          | Get all the categories to which the given area belongs| Dictionary (JSON)
# /area/(\d+)/average_measurement | Get the average measurement for the given area        | Number (JSON)
# /area/(\d+)/number_locations	  | Get the number of locations in the given area         | Number (JSON)
#
# /location	                      | Get all locations                                     | Dictionary (JSON)
# /location/(\d+)           	  | Get location by id                                    | Object (JSON)
# /location/(\d+)/measurement	  | Get all the measurements for the given location id    | Dictionary (JSON)
#
# /category	                      | Get all categories                                    | Dictionary (JSON)
# /category/(\d+)           	  | Get category by id                                    | Object (JSON)

# /measurement	                  | Get all measurement                                   | Dictionary (JSON)
# /measurement/(\d+)           	  | Get measurement by id                                 | Object (JSON)
# =====================================================================================================================

host = '0.0.0.0'
port = 12345

api_help = '\n' \
           '=====================================================================================================================\n' \
           ' Course:       Internet Programming\n' \
           ' Instructor:   Ben Setzer\n' \
           ' Assignment:   #5\n' \
           ' Author:       Dhruval Darji\n' \
           '\n' \
           ' =====================================================================================================================\n' \
           ' =====================================================================================================================\n' \
           ' Overview:\n' \
           ' This script will respond to requests for data from the measurement\n' \
           ' database by sending back data that is JSON serialized.\n' \
           ' The server should listen on any interface at port 12345.\n' \
           ' =====================================================================================================================\n' \
           ' =====================================================================================================================\n' \
           ' Path                             | Function                                              | Return Type\n' \
           ' =====================================================================================================================\n' \
           ' /area	                          | Get a list of all areas                               | Dictionary (JSON)\n' \
           '/area/(\d+)	                      | Get area by id                                        | Object (JSON)\n' \
           ' area/(\d+)/location	          | Get all locations for the given area id               | Dictionary (JSON)\n' \
           ' /area/(\d+)/category	          | Get all the categories to which the given area belongs| Dictionary (JSON)\n' \
           ' /area/(\d+)/average_measurement  | Get the average measurement for the given area        | Number (JSON)\n' \
           ' /area/(\d+)/number_locations	  | Get the number of locations in the given area         | Number (JSON)\n' \
           '\n' \
           ' /location	                      | Get all locations                                     | Dictionary (JSON)\n' \
           ' /location/(\d+)           	      | Get location by id                                    | Object (JSON)\n' \
           ' /location/(\d+)/measurement	  | Get all the measurements for the given location id    | Dictionary (JSON)\n' \
           '\n' \
           ' /category	                      | Get all categories                                    | Dictionary (JSON)\n' \
           ' /category/(\d+)           	      | Get category by id                                    | Object (JSON)\n' \
           '\n' \
           ' /measurement	                  | Get all measurement                                   | Dictionary (JSON)\n' \
           ' /measurement/(\d+)           	  | Get measurement by id                                 | Object (JSON)\n' \
           ' =====================================================================================================================\n' \
           '\n'

# Define Regex for URLs
re_all_areas = re.compile('/area')
re_area_by_id = re.compile('/area/(\d+)')
re_locations_by_area = re.compile('/area/(\d+)/location')
re_categories_by_area = re.compile('/area/(\d+)/category')
re_averages_by_area = re.compile('/area/(\d+)/average_measurement')
re_totals_by_area = re.compile('/area/(\d+)/number_locations')


re_all_locations = re.compile('/location')
re_one_location = re.compile('/location/(\d+)')
re_location_measurements = re.compile('/location/(\d+)/measurement')


re_all_categories = re.compile('/category')
re_one_category = re.compile('/category/(\d+)')


re_all_measurements = re.compile('/measurement')
re_one_measurement = re.compile('/measurement/(\d+)')

re_favicon = re.compile('/favicon.ico')


# ==========================================================================================================

# SQL Statements


# AREA


# Return Areas as a JSON Dictionary.
def get_all_areas():
    conn = sqlite3.connect('measures.sqlite')

    # create a cursor to navigate this database
    c = conn.cursor()

    # Execute an SQL statement; results are stored in the cursor
    c.execute('SELECT * FROM area;')
    rows = c.fetchall()

    # Convert query JSON
    # Convert query to objects of key-value pairs
    objects_list = []
    for row in rows:
        d = collections.OrderedDict()
        d['area_id'] = row[0]
        d['name'] = row[1]
        d['longitude'] = row[2]
        d['latitude'] = row[3]
        objects_list.append(d)

    j = json.dumps(objects_list)
    conn.close()

    return j


# Return one area as a JSON Object.
def get_one_area(area_id):
    conn = sqlite3.connect('measures.sqlite')

    # create a cursor to navigate this database
    c = conn.cursor()

    # Execute an SQL statement; results are stored in the cursor
    c.execute('SELECT * FROM area WHERE area_id = ' + area_id + ';')
    rows = c.fetchall()

    # Convert query JSON
    # Convert query to objects of key-value pairs
    objects_list = []
    for row in rows:
        d = collections.OrderedDict()
        d['area_id'] = row[0]
        d['name'] = row[1]
        d['longitude'] = row[2]
        d['latitude'] = row[3]
        objects_list.append(d)

    j = json.dumps(objects_list[0])
    conn.close()

    return j


# Return Locations by area as a JSON Dictionary.
def get_locations_by_area(area_id):
    conn = sqlite3.connect('measures.sqlite')

    # create a cursor to navigate this database
    c = conn.cursor()

    # Execute an SQL statement; results are stored in the cursor
    c.execute('SELECT * FROM location WHERE location_area =' + area_id + ';')
    rows = c.fetchall()

    # Convert query JSON
    # Convert query to objects of key-value pairs
    objects_list = []
    for row in rows:
        d = collections.OrderedDict()
        d['location_id'] = row[0]
        d['name'] = row[1]
        d['altitude'] = row[2]
        d['location_area'] = row[3]
        objects_list.append(d)

    j = json.dumps(objects_list)
    conn.close()

    return j


# Return Categories as a JSON Dictionary.
def get_categories_by_area(area_id):
    conn = sqlite3.connect('measures.sqlite')

    # create a cursor to navigate this database
    c = conn.cursor()

    # Execute an SQL statement; results are stored in the cursor
    c.execute('SELECT * FROM category ' +
              'INNER JOIN category_area ON category_area.category_id = category.category_id ' +
              'INNER JOIN area ON area.area_id = category_area.area_id ' +
              'WHERE area.area_id = ' + area_id + ';')

    rows = c.fetchall()

    # Convert query JSON
    # Convert query to objects of key-value pairs
    objects_list = []
    for row in rows:
        d = collections.OrderedDict()
        d['category_id'] = row[0]
        d['name'] = row[1]
        d['description'] = row[2]
        objects_list.append(d)

    j = json.dumps(objects_list)
    conn.close()

    return j


# Return the average Measurements for a given Area as a JSON Number.
def get_avg_measurement_by_area(area_id):
    conn = sqlite3.connect('measures.sqlite')

    # create a cursor to navigate this database
    c = conn.cursor()
    # Execute an SQL statement; results are stored in the cursor
    c.execute('SELECT AVG(value) FROM measurement ' +
              'INNER JOIN location ON location.location_id = measurement.measurement_location ' +
              'INNER JOIN area ON area.area_id = location.location_area ' +
              'WHERE area.area_id = ' + area_id + ';')
    average = c.fetchone()[0]

    # Convert query JSON Number

    j = json.dumps(average)
    conn.close()

    return j


# Return the total number of Locations for a given Area as a JSON Number.
def get_total_locations_by_area(area_id):
    conn = sqlite3.connect('measures.sqlite')

    # create a cursor to navigate this database
    c = conn.cursor()

    # Execute an SQL statement; results are stored in the cursor
    c.execute('SELECT COUNT(*) FROM location ' +
              'INNER JOIN area ON area.area_id = location.location_area ' +
              'WHERE area.area_id = ' + area_id + ';')
    total = c.fetchone()[0]

    # Convert query JSON

    j = json.dumps(total)
    conn.close()

    return j


# Locations


# Return all Locations as a JSON Object.
def get_all_locations():
    conn = sqlite3.connect('measures.sqlite')

    # create a cursor to navigate this database
    c = conn.cursor()

    # Execute an SQL statement; results are stored in the cursor
    c.execute('SELECT * FROM location')
    rows = c.fetchall()

    # Convert query JSON
    # Convert query to objects of key-value pairs
    objects_list = []
    for row in rows:
        d = collections.OrderedDict()
        d['location_id'] = row[0]
        d['name'] = row[1]
        d['altitude'] = row[2]
        d['location_area'] = row[3]
        objects_list.append(d)

    j = json.dumps(objects_list)
    conn.close()

    return j


# Return a Location as a JSON Object.
def get_one_location(location_id):
    conn = sqlite3.connect('measures.sqlite')

    # create a cursor to navigate this database
    c = conn.cursor()

    # Execute an SQL statement; results are stored in the cursor
    c.execute('SELECT * FROM location WHERE location_id = ' + location_id)
    rows = c.fetchall()

    # Convert query JSON
    # Convert query to objects of key-value pairs
    objects_list = []
    for row in rows:
        d = collections.OrderedDict()
        d['location_id'] = row[0]
        d['name'] = row[1]
        d['altitude'] = row[2]
        d['location_area'] = row[3]
        objects_list.append(d)

    j = json.dumps(objects_list[0])
    conn.close()

    return j


# Return Measurements by location as a JSON Dictionary.
def get_measurements_by_location(location_id):
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
        d['measurement_id'] = row[0]
        d['value'] = row[1]
        d['measurement_location'] = row[2]
        objects_list.append(d)

    j = json.dumps(objects_list)
    conn.close()

    return j


# Categories


# Return all Categories as a JSON Object.
def get_all_categories():
    conn = sqlite3.connect('measures.sqlite')

    # create a cursor to navigate this database
    c = conn.cursor()

    # Execute an SQL statement; results are stored in the cursor
    c.execute('SELECT * FROM category')
    rows = c.fetchall()

    # Convert query JSON
    # Convert query to objects of key-value pairs
    objects_list = []
    for row in rows:
        d = collections.OrderedDict()
        d['category_id'] = row[0]
        d['name'] = row[1]
        d['description'] = row[2]
        objects_list.append(d)

    j = json.dumps(objects_list)
    conn.close()

    return j


# Return a Category as a JSON Object.
def get_one_category(category_id):
    conn = sqlite3.connect('measures.sqlite')

    # create a cursor to navigate this database
    c = conn.cursor()

    # Execute an SQL statement; results are stored in the cursor
    c.execute('SELECT * FROM category WHERE category_id = ' + category_id)
    rows = c.fetchall()

    # Convert query JSON
    # Convert query to objects of key-value pairs
    objects_list = []
    for row in rows:
        d = collections.OrderedDict()
        d['category_id'] = row[0]
        d['name'] = row[1]
        d['description'] = row[2]
        objects_list.append(d)

    j = json.dumps(objects_list[0])
    conn.close()

    return j


# Measurements


# Return all Measurements as a JSON Object.
def get_all_measurements():
    conn = sqlite3.connect('measures.sqlite')

    # create a cursor to navigate this database
    c = conn.cursor()

    # Execute an SQL statement; results are stored in the cursor
    c.execute('SELECT * FROM measurement')
    rows = c.fetchall()

    # Convert query JSON
    # Convert query to objects of key-value pairs
    objects_list = []
    for row in rows:
        d = collections.OrderedDict()
        d['measurement_id'] = row[0]
        d['value'] = row[1]
        d['measurement_location'] = row[2]
        objects_list.append(d)

    j = json.dumps(objects_list)
    conn.close()

    return j


# Return a Measurement as a JSON Object.
def get_one_measurement(measurement_id):
    conn = sqlite3.connect('measures.sqlite')

    # create a cursor to navigate this database
    c = conn.cursor()

    # Execute an SQL statement; results are stored in the cursor
    c.execute('SELECT * FROM measurement WHERE measurement_id = ' + measurement_id)
    rows = c.fetchall()

    # Convert query JSON
    # Convert query to objects of key-value pairs
    objects_list = []
    for row in rows:
        d = collections.OrderedDict()
        d['measurement_id'] = row[0]
        d['value'] = row[1]
        d['measurement_location'] = row[2]
        objects_list.append(d)

    j = json.dumps(objects_list[0])
    conn.close()

    return j


# ==========================================================================================================


class MyRestHandler(BaseHTTPRequestHandler):

    # Our 404 Message
    BaseHTTPRequestHandler\
        .error_message_format = '<!doctype html>' \
                                '<html>' \
                                '<head>' \
                                '<meta charset="utf-8"/>' \
                                '<meta name="viewport" content="width=device-width, initial-scale=1.0">' \
                                '<title>404 Not Found!</title>' \
                                '</head>' \
                                '<body>' \
                                '<h1>404 Not Found!</h1>' \
                                '<p>Sorry, could not find the requested data.</p>' \
                                '</body>'

    def do_GET(self):

        if re.search(re_favicon, self.path):
            fav = open('/favicon.png')
            self.send_response(200)
            self.send_header('Content-Type', 'image/png')
            self.end_headers()
            self.wfile.write(fav.read())

            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(api_help)
            return

        elif self.path.startswith('/help'):
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(api_help.encode())
            return

        elif self.path.startswith('/measurement'):
            if re.search(re_one_measurement, self.path):
                measurement_id = self.path.split('/')[2]
                measurements = get_one_measurement(measurement_id)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                data = measurements.encode()
                self.wfile.write(data)
                return

            elif re.search(re_all_measurements, self.path):
                measurements = get_all_measurements()
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                data = measurements.encode()
                self.wfile.write(data)
                return

        elif self.path.startswith('/category'):
            if re.search(re_one_category, self.path):
                category_id = self.path.split('/')[2]
                categories = get_one_category(category_id)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                data = categories.encode()
                self.wfile.write(data)
                return

            elif re.search(re_all_categories, self.path):
                categories = get_all_categories()
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                data = categories.encode()
                self.wfile.write(data)
                return

        elif self.path.startswith('/location'):
            if re.search(re_location_measurements, self.path):
                location_id = self.path.split('/')[2]
                measurements = get_measurements_by_location(location_id)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                data = measurements.encode()
                self.wfile.write(data)

            elif re.search(re_one_location, self.path):
                location_id = self.path.split('/')[2]
                locations = get_one_location(location_id)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                data = locations.encode()
                self.wfile.write(data)
                return

            elif re.search(re_all_locations, self.path):
                locations = get_all_locations()
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                data = locations.encode()
                self.wfile.write(data)
                return

        elif self.path.startswith('/area'):
            if re.search(re_totals_by_area, self.path):
                area_id = self.path.split('/')[2]
                total = get_total_locations_by_area(area_id)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                data = total.encode()
                self.wfile.write(data)
                return

            elif re.search(re_averages_by_area, self.path):
                area_id = self.path.split('/')[2]
                average = get_avg_measurement_by_area(area_id)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                data = average.encode()
                self.wfile.write(data)
                return

            elif re.search(re_categories_by_area, self.path):
                area_id = self.path.split('/')[2]
                categories = get_categories_by_area(area_id)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                data = categories.encode()
                self.wfile.write(data)
                return

            elif re.search(re_locations_by_area, self.path):
                area_id = self.path.split('/')[2]
                areas = get_locations_by_area(area_id)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                data = areas.encode()
                self.wfile.write(data)
                return

            elif re.search(re_area_by_id, self.path):
                area_id = self.path.split('/')[2]
                areas = get_one_area(area_id)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                data = areas.encode()
                self.wfile.write(data)
                return

            elif re.search(re_all_areas, self.path) and len(self.path) == 5:
                areas = get_all_areas()
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                data = areas.encode()
                self.wfile.write(data)
                return

        else:
            self.send_error(404, 'Data Not Found: %s' % self.path)
            return

server = HTTPServer((host, port), MyRestHandler)

server.serve_forever()
