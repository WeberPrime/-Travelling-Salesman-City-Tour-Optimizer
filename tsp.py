import argparse
import csv
from collections import namedtuple
from distance import compute_distance_matrix
from tsp_solver import greedy_tsp, two_opt
from geojson_export import export_geojson

Place = namedtuple("Place", ["Name", "Lat", "Lon"])

def read_places(csv_file):
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return [Place(row["Name"], float(row["Lat"]), float(row["Lon"])) for row in reader]

def total_distance(path, distance_matrix):
    return sum(distance_matrix[path[i]][path[i+1]] for i in range(len(path)-1))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True, help="CSV file with places")
    parser.add_argument("--start", required=True, help="Name of the starting location")
    parser.add_argument("--roundtrip", action="store_true", help="Return to start at the end")
    args = parser.parse_args()

    places = read_places(args.csv)
    names = [p.Name for p in places]
    if args.start not in names:
        print(f"Start place '{args.start}' not found in CSV.")
        return

    start_index = names.index(args.start)
    dist_matrix = compute_distance_matrix(places)

    path = greedy_tsp(dist_matrix, start=start_index)
    path = two_opt(path, dist_matrix)
    if args.roundtrip:
        path.append(path[0])  # Return to start

    print("Optimal tour:")
    for i, idx in enumerate(path):
        print(f"{i+1}) {places[idx].Name}")
    print(f"Total distance: {total_distance(path, dist_matrix):.2f} km")

    export_geojson(places, path)

    print("Route written to route.geojson.")

if __name__ == "__main__":
    main()

