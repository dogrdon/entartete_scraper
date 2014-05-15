#!/usr/bin/env python


import csv
import lxml.html
import requests

import time
from datetime import datetime


'''
This script is used to take our csv list of artists and grab additional information about each artist from their dbpedia resource such as:
  -movement they were associated with
  -influences?
  -influenced?
  -dates of birth/death
  -whether they have a wikipedia record or not, in the first place
  -nationality and much, much more.
'''

'''
1) open csv and start to loop
  - for each artist, get from the .rdf file the above items
  - if nothing, make a note of it
  - where should we be logging the fact that some artists will not a page
'''

fname = '../data/artists-full-'+datetime.now().isoformat()+'.csv'

with open('../data/artists_ld.csv', 'r') as file:
  r = csv.reader(file)
  w = csv.writer(open(fname, 'w'))

  header = r.next()

  header.extend(['ntnl', 'mvmnt', 'born', 'died'])

  w.writerow(header)

  for row in r:

    if row[2] != 'nA':


      dom = lxml.html.fromstring(requests.get(row[2]).content)
      mvmnt = []
      ntnl = []
      if dom.cssselect('a[rel="dbpedia-owl:movement"]'):
        for a in dom.cssselect('a[rel="dbpedia-owl:movement"]'):
          mvmnt.append(a.text_content().split(':')[1])
      else:
        mvmnt.append('nA')

      if dom.cssselect('a[rel="dbpedia-owl:nationality"]'):
        for a in dom.cssselect('a[rel="dbpedia-owl:nationality"]'):
          ntnl.append(a.text_content().split(':')[1])
      else:
        ntnl.append('nA')

      if dom.cssselect('span[property="dbpedia-owl:birthDate"]'):
        for s in dom.cssselect('span[property="dbpedia-owl:birthDate"]'):
          dob = s.text_content()
      else:
        dob = 'nA'

      if dom.cssselect('span[property="dbpedia-owl:deathDate"]'):
        for s in dom.cssselect('span[property="dbpedia-owl:deathDate"]'):
          dod = s.text_content()
      else:
        dod = 'nA'

      ntnl = [v.replace('_', ' ') for v in ntnl]
      mvmnt = [v.replace('_', ' ') for v in mvmnt]
      
      print 'adding: ', ntnl, mvmnt, dob, dod, 'for: ', row[1]
      
      row.extend([', '.join(ntnl).encode('utf8'), ', '.join(mvmnt).encode('utf8'), dob, dod])
      
      #row = [v.encode('utf8') for v in row]
      
      w.writerow(row)

      
