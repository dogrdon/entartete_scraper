#!/usr/bin/env python

import csv

'''TODO: Last record should not outout a final comma (,)'''


'''ref: http://www.andrewdyck.com/how-to-convert-csv-data-to-geojson/'''

headers = ['artist_id', 'catalog_id', 'db_id', 'loss_thru', 'artwork_title', 'location', 'date_lost', 'material', 'ek_inven_id', 'uri', 'art_form', 'envelope', 'work_status', 'db_title', 'date', 'copyright', 'inv_orig', 'env_part', 'thumb_url', 'museum_orig', 'artist', 'lat', 'lng']

file = csv.reader(open('./data/entartete_kunst_geocoded_bing2.csv', 'rb'))

template = \
    ''' \
    { "type" : "Feature",
        "id" : %s,
        "geometry" : {
            "type" : "Point",
            "coordinates" : ["%s", "%s"]},
        "properties" : {
            "artist" : "%s",
            "artwork" : "%s",
            "date" : "%s",
            "location" : "%s",
            "url" : "%s",
            "img_src" : "%s",
            "status" : "%s"}
        },
    '''
    
output = \
    '''\
{"type": "FeatureCollection",
    "features": [
    '''
    
count = 0
for row in file:
    count += 1
    if count >= 2:
        art_id = row[2]
        lat = row[22]
        lng = row[23]
        artist = row[21]
        artwork = row[5]
        date = row[15]
        location = row[6]
        url = row[10]
        img_src = row[19]
        status = row[13]
        output += template % (art_id, lng, lat, artist, artwork, date, location, url, img_src, status)

        
output += \
    ''' \
    ]
}
    '''
    

output = output.replace(output[-15], '')
    
#open a new file and dump contents from above
outFile = open("./data/entartete_kunst_geocoded_bing2.geojson", "w")
outFile.write(output)
outFile.close()