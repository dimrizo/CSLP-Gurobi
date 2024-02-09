# Railways and Transport Laboratory, National Technical University of Athens
# Charging Stations Location Problem for Electric Buses (EB-CSLP) - Module to generate random coordinates within a bounding box

import random
from shapely.geometry import Polygon, Point

def main(num_points):
	"""This function calculates random coordinates within a boudning box""" 

	poly = Polygon([(38.107586, 23.734303),
					(38.027126, 23.868836),
					(37.918797, 23.739499),
					(37.983904, 23.616514)])

	min_x, min_y, max_x, max_y = poly.bounds

	counter = 0
	latitudes = {}
	longitudes = {}
	while counter < num_points:
		random_lat = random.uniform(min_x, max_x)
		random_lon = random.uniform(min_y, max_y)
		random_point = Point([random_lat, random_lon])

		if (random_point.within(poly)):
			latitudes[counter+1] = random_lat
			longitudes[counter+1] = random_lon
			counter += 1

	return latitudes, longitudes
