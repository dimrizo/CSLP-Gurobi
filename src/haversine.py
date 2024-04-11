#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Module description: Returns direct distance in meters between two points
import math


def main(lat_1, lon_1, lat_2, lon_2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon_1, lat_1, lon_2, lat_2 = map(math.radians, [lon_1, lat_1, lon_2, lat_2])

    # haversine formula
    dlon = lon_2 - lon_1
    dlat = lat_2 - lat_1
    a = math.sin(dlat / 2)**2 + math.cos(lat_1) * \
        math.cos(lat_2) * math.sin(dlon / 2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles

    print(c * r * 1000)

    return c * r * 1000  # meters


if __name__ == "__main__":
    main(37.9718, 23.7816, 37.9621, 23.7711)
