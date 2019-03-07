"""Calculate the distance in kilometres between each brewery and save the matrix to a file."""

import numpy
import pandas
from haversine import haversine

beer_counts = pandas.read_csv("beer_counts.csv")
breweries_count = len(beer_counts)

distances = numpy.zeros((breweries_count, breweries_count))
for i, i_row in beer_counts.iterrows():
    point_i = (i_row['latitude'], i_row['longitude'])
    for j, j_row in beer_counts.iterrows():
        point_j = (j_row['latitude'], j_row['longitude'])
        distances[i, j] = haversine(point_i, point_j)

numpy.savetxt("distances.csv", distances)


