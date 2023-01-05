import argparse
import pandas as pd
import random
import numpy as np
import reverse_geocoder as rg
from geopy.distance import great_circle

#announcing constats
lat_min, lat_max = -90, 90
long_min, long_max = -180, 180
file_path = ('places.csv')

geocoder_name_key = "name"
geocoder_lat_key = "lat"
geocoder_lon_key = "lon"

name_key = "Name"
lat_key = "Latitude"
lon_key = "Longitude"

someplace_column = "Someplace"
otherplace_column = "Otherplace"
distance_column = "Distance, km"

rounding_constant = 1

if __name__ == "__main__":
#adding if __name__ == "__main__": to avoid reverse_geocoder error

    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", type=int, help="number of randomly generated places")
    args = parser.parse_args()

    # Read in the input data
    if args.n and args.n > 0:
        # Generate n randomly generated places
        places = []

        for i in range(args.n):
            place = {
                name_key: f"Place {i + 1}",
                lat_key: random.uniform(lat_min, lat_max),
                lon_key: random.uniform(long_min, long_max)
            }
            # to make project more fun and interesting I decided to use reverse geocoder to find closest city to random coordinates
            result = rg.search((place[lat_key], place[lon_key]))

            # Update the place dictionary with the closest city and its coordinates
            place[name_key] = result[0][geocoder_name_key]
            place[lat_key] = result[0][geocoder_lat_key]
            place[lon_key] = result[0][geocoder_lon_key]

            places.append(place)

        df = pd.DataFrame(places)

    else:
        # Use the places.csv file as input
        df = pd.read_csv(file_path)

    # Print the input data
    print("\nRandom places", "\n", df)

    # calculating distances

    # Compute the great circle distances between all pairs of places
    distances = []
    for i, place1 in df.iterrows():
        for j, place2 in df.iterrows():
            if i != j:
                distance = round(great_circle((place1[lat_key], place1[lon_key]),
                                        (place2[lat_key], place2[lon_key])).km, rounding_constant)
                distances.append((place1[name_key], place2[name_key], distance))

    # making a dataframe of distances for ease of further data processing
    df_distances = pd.DataFrame(distances, columns=[someplace_column, otherplace_column, distance_column])
    df_distances = df_distances.sort_values(by=[distance_column], ascending=True)
    print("\nCalculating distences between places", "\n", df_distances)
    print("\nLength of df with duplicates:", len(df_distances))

    # removing mirrowing pairs
    df_distances = df_distances.loc[
        pd.DataFrame(np.sort(df_distances[[someplace_column, otherplace_column]], 1), index=df_distances.index).drop_duplicates(
            keep='first').index]
    df_distances = df_distances.reset_index(drop=True)
    print("\nDataframe without duplicates", "\n", df_distances)
    print("\nLength of df without duplicates:", len(df_distances))

    # finding mean distance and pair with distance closest to the mean
    mean_distance = df_distances[distance_column].mean().round(rounding_constant )
    df_closest = df_distances.iloc[(df_distances[distance_column] - mean_distance).abs().round(rounding_constant).argsort()[:1]]
    df_closest = df_closest.reset_index(drop=True)
    print("\nAverage distance:", mean_distance, "\nClosest pair to the average distance value:\n", df_closest)
