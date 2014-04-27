#!/usr/bin/env python

from rdflib import Graph, URIRef
import csv


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

def get_artist_uris():
  '''
  Loop through artist names and get their uris made in quick succession
  '''
  with open('../data/apr-2014/degenerate_artists.csv', 'rb') as file:
    r = csv.reader(file)
    r.next() #skip the header
    for row in r:
      if row[1].startswith('!'):
        pass
      else:
        print create_uri(row[1])
      #print row[1]


def create_uri(artist_name):
  '''
  Create a URI name from a first name last last name first entry in
  the database (ex. Klee, Paul -> Paul_Klee) and return a URI to dbpedia for that person
  '''
  name = artist_name.split(',')

  uri_name = name[1].strip() + '_' + name[0].strip()

  uri = _DBP_BASE + uri_name

  return uri

get_artist_uris()
