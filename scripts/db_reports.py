#!/usr/bin/env python


import sqlite3
import repr
import csv

q_museums = 'SELECT a.museum_orig, count(a.museum_orig) as c FROM artworks a GROUP BY a.museum_orig ORDER BY c DESC'

q_artists = 'SELECT a.artist FROM artists a'


conn = sqlite3.connect('../data/db/entartete_kunst.db')
c = conn.cursor()


def run_query(q):
  for row in c.execute(q):
    print row[0]





run_query(q_artists)
