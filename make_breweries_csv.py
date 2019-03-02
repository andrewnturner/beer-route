"""Pull the data we need from the relevant CSVs and save it to a new file."""

import pandas

breweries = pandas.read_csv("data/breweries.csv", index_col="id")[['name']]

beers = pandas.read_csv("data/beers.csv")
beer_counts = beers.groupby('brewery_id').count()['id'].rename("beers_count")

geocodes = pandas.read_csv("data/geocodes.csv")[['brewery_id', 'latitude', 'longitude']]

with_counts = pandas.merge(breweries, beer_counts, how='inner', left_index=True, right_index=True)
data = pandas.merge(with_counts, geocodes, how='inner', left_index=True, right_on="brewery_id")

data.to_csv("beer_counts.csv", index=False)

