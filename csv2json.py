#!/usr/bin/env python

import csv, json

'''quick grabbed from here: http://www.andymboyle.com/2011/11/02/quick-csv-to-json-parser-in-python/'''


file = open('./data/entartete_kunst_geocoded.csv', 'rU')

csv_read = csv.DictReader( file, fieldnames = ('artist_id', 'catalog_id', 'db_id', 'loss_thru', 'artwork_title', 'location', 'date_lost', 'material', 'ek_inven_id', 'uri', 'art_form', 'envelope', 'work_status', 'db_title', 'date', 'copyright', 'inv_orig', 'env_part', 'thumb_url', 'museum_orig', 'artist', 'lat', 'lng'))

#print next(csv_read) #print the headers for fun
next(csv_read, None) #skip the header

output = json.dumps([row for row in csv_read], indent=2)
print "parsed csv file and ready to print json"

j = open('./data/entartete_kunst_geocoded.json', 'w')

j.write(output)

print "json printed"