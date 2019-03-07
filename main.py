"""
Calculate a route collecting as many beers as possible in a given distance.

The algorithm is simple:
- We have a single parameter `scan`, which is an integer greater than 0.
- At each step, we look at the `scan` nearest breweries which are within range.We then
  choose to visit the one which has the most beers.
- We just keep doing that until we have to go home.

The script tries `scan` from 1 to 9. For this problem `3` is optimal, visiting 77
breweries to collect 304 beer types.
"""

import time

import numpy
import pandas
from haversine import haversine


class Brewery:
    def __init__(self, brewery_id, name, beers_count, location, distances_index):
        self.brewery_id = brewery_id
        self.name = name
        self.beers_count = beers_count
        self.location = location
        self.distances_index = distances_index

    def __str__(self):
        return self.name


class Journey:
    def __init__(self, home):
        self.home = home

        self.breweries = []
        self.final_distance = 0
    
    def record_brewery(self, brewery, distance):
        self.breweries.append((brewery, distance))

    def record_home(self, final_distance):
        self.final_distance = final_distance

    def score(self):
        return sum(brewery.beers_count for brewery, distance in self.breweries)

    def print_out(self):
        print(f"Found {len(self.breweries)} beer factories:")
        print(f"    -> HOME: {self.home} distance 0km")
        beers_collected = 0
        total_distance = 0
        for brewery, distance in self.breweries:
            beers_collected += brewery.beers_count
            total_distance += distance
            print(f"    -> [{brewery.brewery_id}] {brewery.name}: {brewery.location} distance {distance:.0f}km")
        print(f"    <- HOME: {self.home} distance {self.final_distance:.0f}km")
        total_distance += self.final_distance
        print(f"Total distance travelled: {total_distance:.0f}km")
        print(f"Collected {beers_collected} beer types")


beer_counts = pandas.read_csv("beer_counts.csv")
distances = numpy.loadtxt("distances.csv")

breweries = [
    Brewery(row['brewery_id'], row['name'], row['beers_count'], (row['latitude'], row['longitude']), i)
    for i, row in beer_counts.iterrows()
]

def find_journey(home_location, start_fuel, scan):
    home_distances = [
        haversine(home_location, (row['latitude'], row['longitude']))
        for i, row in beer_counts.iterrows()
    ]

    current_fuel = start_fuel
    beers_collected = 0
    visited = set()

    journey = Journey(home_location)

    available_breweries = sorted(breweries, key=lambda b: home_distances[b.distances_index])[:scan]
    selected_brewery = max(available_breweries, key=lambda b: b.beers_count)
    selected_distance = home_distances[selected_brewery.distances_index]

    current_fuel -= selected_distance
    beers_collected += selected_brewery.beers_count
    visited.add(selected_brewery)

    journey.record_brewery(selected_brewery, selected_distance)

    while current_fuel > 0:
        previous_brewery = selected_brewery
        available_breweries = filter(
            lambda b: (b not in visited) and
                (home_distances[b.distances_index] < current_fuel - distances[previous_brewery.distances_index, b.distances_index]),
            breweries
        )
        candidates = sorted(
            available_breweries,
            key=lambda b: distances[previous_brewery.distances_index, b.distances_index]
        )[:scan]
        
        if not candidates:
            break
        
        selected_brewery = max(candidates, key=lambda b: b.beers_count)
        selected_distance = distances[previous_brewery.distances_index, selected_brewery.distances_index]

        current_fuel -= selected_distance
        beers_collected += selected_brewery.beers_count
        visited.add(selected_brewery)

        journey.record_brewery(selected_brewery, selected_distance)

    journey.record_home(home_distances[selected_brewery.distances_index])

    return journey

if __name__ == "__main__":
    # (longitude, latitude) of where to start and end.
    home_location = (51.355468, 11.100790)
    # Maximum distance to travel in kilometres.
    start_fuel = 2000

    start = time.time()
    
    best_journey = None
    best_score = 0
    best_scan = None
    for i in range(1, 10):
        journey = find_journey(home_location, start_fuel, i)
        if journey.score() > best_score:
            best_journey = journey
            best_score = journey.score()
            best_scan = i

    end = time.time()

    print(f"Scan {best_scan}")
    print("")
    best_journey.print_out()

    print("")
    print(f"Program took {end-start}s")
        
    