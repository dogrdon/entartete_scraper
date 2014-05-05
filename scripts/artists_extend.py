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
This script is used to take our csv list of artists and our new rdf grapch and grab additional information about each artist in the ~/data/degenerate_artisists.csv file such as:
  -movement they were associated with
  -influences
  -influenced
  -dates of birth/death
  -whether they have a wikipedia record or not
  -nationality and much, much more.
'''

'''
1) open csv and start to loop
  - for each artist, get from the .rdf file the above items
  - if nothing, make a note of it
  - where should we be logging the fact that some artists will not have db
'''
