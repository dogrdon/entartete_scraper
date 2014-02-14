#!/usr/bin/env python

import csv



'''ref: http://www.andrewdyck.com/how-to-convert-csv-data-to-geojson/'''

headers = ['artist_id', 'catalog_id', 'db_id', 'loss_thru', 'artwork_title', 'location', 'date_lost', 'material', 'ek_inven_id', 'uri', 'art_form', 'envelope', 'work_status', 'db_title', 'date', 'copyright', 'inv_orig', 'env_part', 'thumb_url', 'museum_orig', 'artist', 'lat', 'lng']

file = csv.reader(open('./data/entartete_kunst_geocoded.csv', 'rb'))

template = \
    ''' \
    { "type": "Feature",
        "id": %s,
        "geometry":{
            "type": "Point"
            "coordinates": ["%s", "%s"]},
        "properties": {
            "artist": "%s",
            "artwork": "%s",
            "date": "%s",
            "location": "%s",
            "url": "%s",
            "img_src": "%s",
            "status: "%s"}
        },
    '''
    
output = \
    '''\
{"type": "FeatureCollection,
    {"features": [
    '''
    
count = 0
for row in file:
    count += 1
    if count >= 2:
        art_id = row[2]
        lat = row[21]
        lng = row[22]
        artist = row[20]
        artwork = row[4]
        date = row[14]
        location = row[5]
        url = row[9]
        img_src = row[18]
        status = row[12]
        output += template % (art_id, lat, lng, artist, artwork, date, location, url, img_src, status)
        
output += \
    ''' \
    ]
}
    '''
    
#open a new file and dump contents from above
outFile = open("./data/entartete_kunst_geocoded.geojson", "w")
outFile.write(output)
outFile.close()