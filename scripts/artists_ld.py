#!/usr/bin/env python
# coding=utf-8

from rdflib import Graph, URIRef
import csv
import io
import os
from repr import repr
import urllib
import time
from datetime import datetime

'''
This script goes through our set of artist names, goes to dbpedia and pulls down each of there resources into a triple store .rdf file
'''

filenamern = '../data/artists-'+datetime.now().isoformat()+'.rdf'

_DBP_BASE = "http://dbpedia.org/resource/"


def read_graph(graph):

  for stmt in graph.subject_objects(URIRef("http://dbpedia.org/ontology/movement")):
    print str(stmt[0]), 'was part of the', str(stmt[1]), 'movement'



def get_artist_uris():
  '''
  Loop through artist names and get their uris made in quick succession
  '''

  with open('../data/apr-2014/degenerate_artists.csv', 'rb') as file:

    print 'this will print to', filenamern, 'when finished'

    time.sleep(4)


    r = csv.reader(file)
    w = csv.writer(open('../data/artists_ld.csv', 'w'))

    header = r.next() #skip the header
    header.extend(['uri'])

    w.writerow(header)

    for row in r:
      if row[1].startswith('!'):

        print 'nothing to add'
        row.extend([str('nA')])
        w.writerow(row)
        pass
      else:
      #if row[1].startswith('A'):
        print "now adding record for: ", row[1]

        this_uri = create_uri(row[1])

        g.parse(this_uri)

        print "your rdf graph is: ", len(g), "long"

        #add the uri to the new csv file
        row.extend([str(this_uri)])

        w.writerow(row)

    '''
    print 'generating graph...'
    time.sleep(5)
    print 'saving graph as rdf file'
    time.sleep(5)

    with open(filenamern, 'w') as ld:
      ld.write(g.serialize(format='xml'))
      ld.close
    '''

    #try:
    #  g.serialize(filenamern, format='pretty-xml')
    #except Exception as err:
    #  print 'you got an error:', err

    return g


def create_uri(artist_name):
  '''
  Create a URI name from a first name last last name first entry in
  the database (ex. Klee, Paul -> Paul_Klee) and return a URI to dbpedia for that person
  '''
  artist_name = artist_name

  name = artist_name.split(",")

  uri_name = "%s_%s" % (name[1].strip(), name[0].strip())

  uri_name = uri_name.replace(' ', '_')

  uri_name_esc = urllib.quote(uri_name) #hacky work around for unicode problems

  uri = "http://dbpedia.org/resource/" + uri_name_esc

  return uri



if __name__ == "__main__":
  g = Graph()
  get_artist_uris()
  #read_graph(g)
