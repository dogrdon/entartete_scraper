#!/usr/bin/env python
# coding=utf-8

import csv
import lxml.html
import requests

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
  - where should we be logging the fact that some artists will not have db
'''


with open('../data/artists_ld.csv', 'r') as file:
  r = csv.reader(file)
  w = csv.writer(open('../data/artists_full.csv', 'w'))

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

      print 'adding: ', ntnl, mvmnt, dob, dod, 'for: ', row[1]
      row.extend([', '.join(ntnl), ', '.join(mvmnt), str(dob), str(dod)])
      w.writerow(row)

      '''failing here
      ["Expressionism", "Berlin_Secession", "Der_Blaue_Reiter", "Die_Brücke", "November_Group_(German)"]
      '''
