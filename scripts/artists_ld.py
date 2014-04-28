#!/usr/bin/env python
# coding=utf-8

from rdflib import Graph, URIRef
import csv
import io
import os
from repr import repr
import urllib


'''
This script is used to grad additional information about each artist in the ~/data/degenerate_artisists.csv file such as:
  -movement they were associated with
  -influences
  -influenced
  -dates of birth/death
  -whether they have a wikipedia record or not
  -nationality and much, much more.
'''


_DBP_BASE = "http://dbpedia.org/resource/"

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
        print "now adding record for: ", row[1]

        g.parse(create_uri(row[1]))

        print "your rdf graph is: ", len(g), "long"

        #print repr(row[1])
    #print "your rdf graph is: ", len(g), "long"


def create_uri(artist_name):
  '''
  Create a URI name from a first name last last name first entry in
  the database (ex. Klee, Paul -> Paul_Klee) and return a URI to dbpedia for that person
  '''
  artist_name = artist_name

  name = artist_name.split(",")

  uri_name = "%s_%s" % (name[1].strip(), name[0].strip())

  uri_name_esc = urllib.quote(uri_name) #hacky work around for unicode problems

  uri = "http://dbpedia.org/resource/" + uri_name_esc

  return uri



if __name__ == "__main__":
  g = Graph()
  get_artist_uris()
