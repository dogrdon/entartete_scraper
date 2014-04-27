#!/usr/bin/env python

from rdflib import Graph, URIRef

'''
This script is used to grad additional information about each artist in the ~/data/degenerate_artisists.csv file such as:
  -movement they were associated with
  -influences
  -influenced
  -dates of birth/death
  -whether they have a wikipedia record or not
  -nationality and much, much more.
'''


_DBP_BASE = 'http://dbpedia.org/page/'






def create_uri(artist_name):
  '''
  Function to create a URI name from a first name last last name first entry in
  the database (ex. Klee, Paul -> Paul_Klee) and return a URI to dbpedia for that person
  '''
  name = artist_name.split(',')

  uri_name = name[1].strip() + '_' + name[0].strip()

  uri = _DBP_BASE + uri_name

  return uri
