# Beer Route

## How to run

### Preprocessing

1. Run `python make_breweries_csv.py` to generate `beer_counts.csv`.
2. Run `python make_distance_matrix.py` to generate `distances.csv`.

### Finding the route

1. Run `python main.py`. The calculated route is printed to console.

## Configuring

Change the `home_location` and `start_fuel` parameters to find routes from
other locations and of different lengths.