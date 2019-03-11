from urllib.request import urlopen
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from zipfile import ZipFile
import json

STATESHAPEFILEURL = 'https://www.census.gov/geo/tiger/GENZ2017/shp/cb_2017_us_state_500k.zip'
USSHAPEFILEURL = 'https://www.census.gov/geo/tiger/GENZ2017/shp/cb_2017_us_nation_5m.zip'

def main():
    # download the shapefiles, unzip them
    

    # turn the shapefiles into geojson files
    # take the coordinates and turn them into GeoJson Points
    # combine the nation GsoJson and states GeoJson and locations GeoJson into one FeatureCollection
    # project single GeoJson file
    # then break features back out into separate geojson files
    # turn these GeoJson files into topojson files and combine them into a single topojson file
    # then do all the quantizing and simplifying on this one file

def downloadAndCreateZipFile(url, filename):
    with open(filename, 'wb') as f:
        f.write(open(url).read())