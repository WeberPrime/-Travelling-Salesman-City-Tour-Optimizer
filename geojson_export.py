import json

def export_geojson(places, path, filename="route.geojson"):
    coordinates = [[places[i].Lon, places[i].Lat] for i in path]
    geojson = {
        "type": "FeatureCollection",
        "features": [{
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": coordinates
            },
            "properties": {
                "name": "Optimized Route"
            }
        }]
    }
    with open(filename, "w") as f:
        json.dump(geojson, f, indent=2)
