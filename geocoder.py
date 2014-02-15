#!/usr/bin/env python

from geopy import geocoders
import csv
import keys

_BING_API = keys.bing_api

g = geocoders.GoogleV3()
b = geocoders.Bing(_BING_API, timeout=60)

with open('./data/entartete_kunst_full_14FEB2014.csv', 'rb') as file:
    r = csv.reader(file)
    w = csv.writer(open('./data/entartete_kunst_geocoded_bing2.csv', 'w'))
    header = r.next()
    header.extend(['lat', 'lng'])
    w.writerow(header)
    
    unknown = 0
    no_res = 0
    total = 0
    success = 0
    for row in r:
        total += 1
        results = b.geocode(row[6], exactly_one=False)
             
        if row[6] != 'NA' and row[6] != 'unbekannt':
            if results:
                
                place, (lat, lng) = results[0]
                row.extend([str(lat), str(lng)])
                print total, "- adding for %s - %.5f, %.5f" % (row[6], lat, lng) 
                w.writerow(row)
                success += 1
            else:
                no_res += 1
                print total, '- no results for: ', row[6]
                
        else:
            unknown += 1
            print total, '- location is unknown: ', row[6]
            
    print 'All Done! Total Geocodes: %i, Unknown: %i, Successfully Geocoded: %i, No Results: %i' % (total, unknown, success, no_res)
    print 'Success rate today = ', round(float(success)/float(total)*100), '%'
            
    
            
        
            
            
