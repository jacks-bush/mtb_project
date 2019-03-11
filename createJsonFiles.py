from urllib.request import urlopen
from zipfile import ZipFile
import json
import subprocess

BASE_SHAPE_FILE_URL = 'https://www.census.gov/geo/tiger/GENZ2017/shp/'
STATE_SHAPE_FILE_NAME = 'cb_2017_us_state_500k.zip'
NATION_SHAPE_FILE_NAME = 'cb_2017_us_nation_5m.zip'


def main():
    # download the shapefiles, unzip them
    downloadAndUnzipFile(STATE_SHAPE_FILE_NAME, 'shapefiles/states.zip')
    downloadAndUnzipFile(NATION_SHAPE_FILE_NAME, 'shapefiles/nation.zip')

    # turn the shapefiles into geojson files
    subprocess.run(
        'shp2json shapefiles/cb_2017_us_nation_5m.shp -o shapefiles/nation.json')
    subprocess.run(
        'shp2json shapefiles/cb_2017_us_state_500k.shp -o shapefiles/states.json')

    # take the coordinates and turn them into GeoJson Points
    test = createGeoJsonStringForPoints()
    # combine the nation GsoJson and states GeoJson and locations GeoJson into one FeatureCollection
    # project single GeoJson file
    # then break features back out into separate geojson files
    # turn these GeoJson files into topojson files and combine them into a single topojson file
    # then do all the quantizing and simplifying on this one file
    pass


def downloadAndUnzipFile(url, filename):
    # download and save file
    with open(filename, 'wb') as f:
        f.write(urlopen(url).read())
    # extract contents
    with ZipFile(filename) as z:
        z.extractall()


def createGeoJsonStringForPoints():
    # load featured rides json
    jsonObj = json.load(open('featuredRides.json', 'r', encoding='utf-8'))

    # create feature list
    features = []

    for rideObj in jsonObj:
        # create a feature dict with a point dict as a geometry value and all the properties from the featured ride
        features.append({
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [rideObj.long, rideObj.lat]
            },
            'properties': rideObj
        })
    
    # create outer Features dict and use json.dumps to get geojson string
    return json.dumps({'type':'FeatureCollection', 'features': features})

main()
