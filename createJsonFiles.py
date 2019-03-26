from urllib.request import urlopen
from zipfile import ZipFile
import json
import subprocess

BASE_SHAPE_FILE_URL = 'https://www2.census.gov/geo/tiger/GENZ2017/shp/'
STATE_SHAPE_FILE_NAME = 'cb_2017_us_state_500k.zip'
NATION_SHAPE_FILE_NAME = 'cb_2017_us_nation_5m.zip'


def main():
    # download the shapefiles, unzip them
    #     downloadAndUnzipFile(STATE_SHAPE_FILE_NAME, 'states.zip')
    #     downloadAndUnzipFile(NATION_SHAPE_FILE_NAME, 'nation.zip')

    # turn the shapefiles into geojson filesS
    subprocess.call(
        'shp2json cb_2017_us_nation_5m.shp -o nation.json', shell=True)
    subprocess.call(
        'shp2json cb_2017_us_state_500k.shp -o states.json', shell=True)

    # take the coordinates and turn them into GeoJson Points
    # write this out to a file
    with open('points.json', 'w', encoding='utf-8') as f:
        f.write(createGeoJsonStringForPoints())

    # now project all three files
    subprocess.call("geoproject 'd3.geoAlbersUsa(^^^).fitSize([960, 600], d^^^)' nation.json -o nation-albers.json", shell=True)
    subprocess.call("geoproject 'd3.geoAlbersUsa().fitSize([960, 600], d)' states.json > states-albers.json", shell=True)
    subprocess.call("geoproject 'd3.geoAlbersUsa().fitSize([960, 600], d)' points.json > points-albers.json", shell=True)

    # combine these three geojson files into one single topojson file
    subprocess.call('geo2topo nation=nation-albers.json states=states-albers.json points=points-albers.json > combined.json', shell=True)

    # combine the nation GsoJson and states GeoJson and locations GeoJson into one FeatureCollection
    # just get features attribute from both nation.json and states.json and add them to points geojson
    # or perhaps should just create one topojson file first and then project that all at once?
    # nationJson = json.load(open('nation.json', 'r', encoding='utf-8'))
    # statesJson = json.load(open('states.json', 'r', encoding='utf-8'))
    # project single GeoJson file
    # then break features back out into separate geojson files
    # turn these GeoJson files into topojson files and combine them into a single topojson file
    # then do all the quantizing and simplifying on this one file
    pass


def downloadAndUnzipFile(url, filename):
    # download and save file
    with open(filename, 'wb') as f:
        f.write(urlopen(BASE_SHAPE_FILE_URL + url).read())
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
                'coordinates': [rideObj['long'], rideObj['lat']]
            },
            'properties': rideObj
        })

    # create outer Features dict and use json.dumps to get geojson string
    return json.dumps({'type': 'FeatureCollection', 'features': features})


main()
