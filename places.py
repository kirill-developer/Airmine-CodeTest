import argparse
import pandas as pd
import random
import numpy as np
import reverse_geocoder as rg
from geopy.distance import great_circle

if __name__ == "__main__":
# adding if __name__ == "__main__": to avoid reverse_geocoder error

    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", type=int, help="number of randomly generated places")
    args = parser.parse_args()

    # Read in the input data
    if args.n:
        # Generate n randomly generated places
        places = []

        for i in range(args.n):
            place = {
                "Name": f"Place {i + 1}",
                "Latitude": random.uniform(-90, 90),
                "Longitude": random.uniform(-180, 180)
            }
            # to make project more fun and interesting I decided to use reverse geocoder to find closest city to random coordinates
            result = rg.search((place["Latitude"], place["Longitude"]))
            city = result[0]["name"]
            lat = result[0]["lat"]
            lon = result[0]["lon"]

            # Update the place dictionary with the closest city and its coordinates
            place["Name"] = city
            place["Latitude"] = lat
            place["Longitude"] = lon

            places.append(place)

        df = pd.DataFrame(places)

    else:
        # Use the places.csv file as input
        df = pd.read_csv("places.csv")

    # Print the input data
    print("\nRandom places", "\n", df)

    # calculating distances

    # Compute the great circle distances between all pairs of places
    distances = []
    for i, place1 in df.iterrows():
        for j, place2 in df.iterrows():
            if i != j:
                distance = great_circle((place1["Latitude"], place1["Longitude"]),
                                        (place2["Latitude"], place2["Longitude"])).km
                distances.append((place1["Name"], place2["Name"], distance))

    # making a dataframe of distances for ease of further data processing
    df_distances = pd.DataFrame(distances, columns=['Place1', 'Place2', 'Distance'])
    df_distances = df_distances.sort_values(by=['Distance'], ascending=True)
    print("\nCalculating distences between places", "\n", df_distances)
    print("\nLength of df with duplicates:", len(df_distances))

    # removing mirrowing pairs
    df_distances = df_distances.loc[
        pd.DataFrame(np.sort(df_distances[['Place1', 'Place2']], 1), index=df_distances.index).drop_duplicates(
            keep='first').index]
    df_distances = df_distances.reset_index(drop=True)
    print("\nDataframe without duplicates", "\n", df_distances)
    print("\nLength of df without duplicates:", len(df_distances))

    # finding mean distance and pair with distance closest to the mean
    mean_distance = df_distances['Distance'].mean().round(3)
    df_closest = df_distances.iloc[(df_distances['Distance'] - mean_distance).abs().argsort()[:1]]
    df_closest = df_closest.reset_index(drop=True)
    print("\nAverage distance:", mean_distance, "\nClosest pair to the average distance value:\n", df_closest)
