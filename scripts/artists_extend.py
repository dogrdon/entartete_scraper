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


fname = '../data/artists-full-'+datetime.now().isoformat()+'.csv'

with open('../data/artists_ld.csv', 'r') as file:
  r = csv.reader(file)
  w = csv.writer(open(fname, 'w'))

  header = r.next()

  header.extend(['ntnl', 'mvmnt', 'born', 'died', 'subj_terms'])

  w.writerow(header)

  for row in r:

    if row[2] != 'nA':


      dom = lxml.html.fromstring(requests.get(row[2]).content)
      mvmnt = []
      ntnl = []
      subj = []
      if dom.cssselect('a[rel="dbpedia-owl:movement"]'):
        for a in dom.cssselect('a[rel="dbpedia-owl:movement"]'):
          mvmnt.append(a.text_content().split(':')[1])

      elif dom.cssselect('span[property="dbpprop:movement"]'):
        for b in dom.cssselect('span[property="dbpprop:movement"]'):
          mvmnt.append(b.text_content().split(':')[1])

      else:
        mvmnt.append('nA')

      if dom.cssselect('a[rel="dbpedia-owl:nationality"]'):
        for a in dom.cssselect('a[rel="dbpedia-owl:nationality"]'):
          ntnl.append(a.text_content().split(':')[1])

      elif dom.cssselect('span[property="dbpprop:nationality"]'):
        for b in dom.cssselect('span[property="dbpprop:nationality"]'):
          ntnl.append(b.text_content())

      else:
        ntnl.append('nA')

      if dom.cssselect('span[property="dbpedia-owl:birthDate"]'):
        for a in dom.cssselect('span[property="dbpedia-owl:birthDate"]'):
          dob = a.text_content()

      elif dom.cssselect('span[property="dbpprop:birthDate"]'):
        for b in dom.cssselect('span[property="dbpprop:birthDate"]'):
          dob = b.text_content()

      else:
        dob = 'nA'

      if dom.cssselect('span[property="dbpedia-owl:deathDate"]'):
        for a in dom.cssselect('span[property="dbpedia-owl:deathDate"]'):
          dod = a.text_content()

      elif dom.cssselect('span[property="dbpprop:deathDate"]'):
        for b in dom.cssselect('span[property="dbpprop:deathDate"]'):
          dod = b.text_content()

      else:
        dod = 'nA'

      if dom.cssselect('a[rel="dcterms:subject"]'):
        for a in dom.cssselect('a[rel="dcterms:subject"]'):
          subj.append(a.text_content().split(':')[1])
      else:
        subj.append('nA')

      ntnl = [v.replace('_', ' ') for v in ntnl]
      mvmnt = [v.replace('_', ' ') for v in mvmnt]

      print 'adding: ', ntnl, mvmnt, dob, dod, subj, 'for: ', row[1]

      row.extend([', '.join(ntnl).encode('utf8'), ', '.join(mvmnt).encode('utf8'), dob, dod, ', '.join(subj).encode('utf8')])


      w.writerow(row)
