This project is a Code test for backend Developer role at Airmine

Performed by: Kirill Izmikov

Date: 05.01.2023

Description:

 - Program takes one optional integer argument n using argparse library (https://docs.python.org/3/library/argparse.html)

 - If no argument is given, the program will use places.csv as input

 - If n is given, program will randomly generate n places as input. In the beginning random coordinates are generated, then to make project more fun and interesting I decided to use reverse geocoder (https://pypi.org/project/reverse_geocoder/) to find the closest city to random coordinates generated

 - Places are added in Pandas dataframe

 - Program finds the air distance (great circle distance) between all pairs of places using great_circle library from geopy (https://geopy.readthedocs.io/en/stable/index.html?highlight=great_circle) and discards pairs
having the same pair of places as another pair

 - At the end program writes out all place pairs and distances by ascending distance. Also it finds the average distance and the place pair and corresponding
distance having the distance closest to the average value

Instructions on setup and use:

Example: 

 - For 15 places run in terminal: python3 places.py -n 15
 - To get places from places.csv run in terminal: python3 places.py
