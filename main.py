from plot_coordinates import plot_coordinates_on_map

# Your Mapbox access token

# Coordinates dictionaries
tcK = {1: 37.9718, 2: 37.9812, 3: 38.0355, 4: 37.9828, 5: 38.0455, 6: 37.9712, 7: 38.0585, 8: 37.9822, 9: 37.9612, 10: 38.0555}
tyK = {1: 23.7816, 2: 23.7345, 3: 23.7695, 4: 23.7716, 5: 23.7445, 6: 23.7685, 7: 23.7225, 8: 23.7595, 9: 23.7316, 10: 23.7795}
tcV = {1: 37.9733, 2: 38.0012, 3: 38.0088, 4: 37.9932}
tyV = {1: 23.6689, 2: 23.6737, 3: 23.7629, 4: 23.7930}

mapbox_key = "pk.eyJ1IjoiZGltcml6byIsImEiOiJjbHM0b2N5ejUxYWlsMmlwaWtlbmkzYzh0In0.A09Dlb2ZoNblEfuL-WnOQw"

# Call the function to plot coordinates for all dictionaries
plot_coordinates_on_map(tcK, tyK, tcV, tyV, mapbox_key)