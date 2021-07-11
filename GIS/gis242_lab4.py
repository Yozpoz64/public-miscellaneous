# GISCI 242 Lab 4
# Restaurant data obtainer
#   -obtains yelp data through API
#   -formats data and dumps in csv
#   -prints outputted csv data
# Info
# Created by: Samuel Kolston
# Last edited: 130520 1819

import requests
import csv
import datetime
import pandas

# Define constants
# Constant variables that will not change. used for default values that may or may not be replaced with a custom user
#   input, the yelp link being queried, my personal API key
DF_LIMIT = 20
DF_RADIUS = 500
DF_POINT = {'lat': -36.850591, 'lon': 174.767922}
DF_CATEGORY = "restaurants, All"
ENDPOINT = 'https://api.yelp.com/v3/businesses/search'
HEADERS = {'Authorization': 'Bearer dWzWoi_YAVtXv0uXUuiGSNmw0F9oqMysRgMXSoA0S7MOj8MfSJ4kZRx91t0t'
                            'ghrsu1KtzPqPWTeZHo0h0UkX-mMJhV9kIOJmh9Uh7M9RqgsPBWVTdwtka6Qmyr2sXnYx'}

properties = [['name', 'rating', 'url', 'price', 'lat', 'long', 'category']]
params = {'latitude': str(DF_POINT['lat']), 'longitude': str(DF_POINT['lon']), 'limit': str(DF_LIMIT),
          'radius': str(DF_RADIUS), 'categories': DF_CATEGORY}

for value in params:
    new_value = input("Input value for {} (default: {}): ".format(value, params[str(value)]))
    if new_value:
        params[value] = new_value

payload = requests.get(ENDPOINT, params=params, headers=HEADERS).json()

# Convert payload from yelp from a dictionary/array to a list which is easier to work with
# Iterates through all of the businesses, adding each attribute of the business into a nested list (properties)
for business in payload['businesses']:

    # Checks if the business has a price attribute, and if it doesn't to simply add 'null' in the price column
    if 'price' in business:
        price = business['price']
    else:
        price = "null"
    properties.append([str(business['name']), str(business['rating']), str(business['url']), str(price),
                       str(business['coordinates']['latitude']), str(business['coordinates']['longitude']),
                       str(business['categories'][0]['title'])])

filename = "yelpdata_{}.csv".format(datetime.datetime.now().strftime("%d%m%y-%H%M%S"))
with open(filename, 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerows(properties)

print("\nSaved '{}' with {} entries (including column titles):".format(csv_file.name, len(properties)))
csv_file.close()

output = pandas.read_csv(filename)
pandas.set_option('display.max_colwidth', 10)
print(output)


