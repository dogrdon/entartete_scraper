#!/usr/bin/env python

from geopy import geocoders
import csv
import keys

_BING_API = keys.bing_api

g = geocoders.GoogleV3()
b = geocoders.Bing(_BING_API)

with open('./data/entartete_kunst_full_11FEB2014.csv', 'rb') as file:
    r = csv.reader(file)
    w = csv.writer(open('./data/entartete_kunst_geocoded.csv', 'w'))
    header = r.next()
    header.extend(['lat', 'lng'])
    w.writerow(header)
    
    for row in r:
        results = g.geocode(row[5], exactly_one=False)
             
        
        if results:
            place, (lat, lng) = results[0]
            row.extend([str(lat), str(lng)])
            print "adding: %.5f, %.5f" % (lat, lng) 
            w.writerow(row)
        else:
            print 'no results'
            
        
            
            
