import json
from haversine import haversine

station_coordinates = {
    "Melbourne (Olympic Park)": {"lat": -37.8, "lon": 145.0, "total_count": 0},
    "Melbourne Airport": {"lat": -37.7, "lon": 144.8, "total_count": 0},
    "Avalon": {"lat": -38.0, "lon": 144.5, "total_count": 0},
    "Cerberus": {"lat": -38.4, "lon": 145.2, "total_count": 0},
    "Coldstream": {"lat": -37.7, "lon": 145.4, "total_count": 0},
    "Essendon Airport": {"lat": -37.7, "lon": 144.9, "total_count": 0},
    "Fawkner Beacon": {"lat": -37.9, "lon": 144.9, "total_count": 0},
    "Ferny Creek": {"lat": -37.9, "lon": 145.3, "total_count": 0},
    "Frankston (Ballam Park)": {"lat": -38.2, "lon": 145.2, "total_count": 0},
    "Frankston Beach": {"lat": -38.1, "lon": 145.1, "total_count": 0},
    "Geelong Racecourse": {"lat": -38.2, "lon": 144.4, "total_count": 0},
    "Laverton": {"lat": -37.9, "lon": 144.8, "total_count": 0},
    "Moorabbin Airport": {"lat": -38.0, "lon": 145.1, "total_count": 0},
    "Point Cook": {"lat": -37.9, "lon": 144.8, "total_count": 0},
    "Point Wilson": {"lat": -38.1, "lon": 144.5, "total_count": 0},
    "Rhyll": {"lat": -38.5, "lon": 145.3, "total_count": 0},
    "Scoresby": {"lat": -37.9, "lon": 145.3, "total_count": 0},
    "Sheoaks": {"lat": -37.9, "lon": 144.1, "total_count": 0},
    "South Channel Island": {"lat": -38.3, "lon": 144.8, "total_count": 0},
    "St Kilda Harbour RMYS": {"lat": -37.9, "lon": 145.0, "total_count": 0},
    "Viewbank": {"lat": -37.7, "lon": 145.1, "total_count": 0}
    
}

input_path = "raw2.json"

# Reading JSON data from the file
with open(input_path, "r") as json_file:
    data = json.load(json_file)


for i in data:
    long  = i["geometry"]["coordinates"][0]
    lat = i["geometry"]["coordinates"][1]
    min = 10000
    name = ""
    for st in station_coordinates:
        a = haversine((lat,long),(station_coordinates[st]["lat"],station_coordinates[st]["lon"]))
        if a < min:
            name = st
            min = a
    i["nearest_station"] = name
    i["nearest_station_distance"] = min
    station_coordinates[name]["total_count"] += 1

output_path = "connected.json"

# Writing JSON data to the file
with open(output_path, "w") as json_file:
    json.dump(data, json_file, indent=4)


output_path2 = "results.json"

# Writing JSON data to the file
with open(output_path2, "w") as json_file:
    json.dump(station_coordinates, json_file, indent=4)


