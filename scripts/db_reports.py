#!/usr/bin/env python


import sqlite3
import repr
import csv

q_museums = 'SELECT a.museum_orig, count(a.museum_orig) as c FROM artworks a GROUP BY a.museum_orig ORDER BY c DESC LIMIT 10;'

q_status = 'SELECT a.work_status, count(a.work_status) as c FROM artworks a GROUP BY a.work_status ORDER BY c DESC LIMIT 10;'

q_format = 'SELECT a.art_form, count(a.art_form) as c FROM artworks a GROUP BY a.art_form ORDER BY c DESC LIMIT 10;'

q_mostprint = 'SELECT b.artist, count(a.artist_id) as c FROM artworks a, artists b WHERE a.artist_id = b.id AND a.art_form = "Druckgraphik" GROUP BY b.artist ORDER BY c DESC LIMIT 20;'

q_mostworks = 'SELECT b.artist, count(a.artist_id) as c FROM artworks a, artists b WHERE a.artist_id = b.id GROUP BY b.artist ORDER BY c DESC LIMIT 50;'

q_ageattime = 'SELECT b.artist, 1937 - b.born_yr as age FROM artists b WHERE b.born_yr != "nA" AND 1937 < b.died_yr ORDER BY age DESC;'


conn = sqlite3.connect('../data/db/entartete_kunst.db')
c = conn.cursor()


def run_query(q):
  for row in c.execute(q):
    print row[0], row[1]






print 'museums========='
run_query(q_museums)

print 'work status========='
run_query(q_status)

print 'top 10 formats======='
run_query(q_format)

print 'artists with most work in the database'
run_query(q_mostprint)

print 'artist with most works under Printmaking==='
run_query(q_mostworks)

print 'age of artist at time of exhibition==='
run_query(q_ageattime)
