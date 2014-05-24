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

q_avgage = 'SELECT AVG(1937 - b.born_yr) as avg FROM artists b WHERE b.born_yr != "nA" AND 1937 < b.died_yr;'

q_freqsterms = 'SELECT s.subject, count(s.subject) as c FROM subject_terms s GROUP BY s.subject ORDER BY c DESC LIMIT 20;'

q_cmderx = 'SELECT b.artist  FROM subject_terms s, artists b WHERE b.id = s.id AND s.subject = "Commanders_Crosses_of_the_Order_of_Merit_of_the_Federal_Republic_of_Germany";'

q_titlefreq = 'SELECT a.artwork_title, count(a.artwork_title) as c FROM artworks a GROUP BY a.artwork_title ORDER BY c DESC LIMIT 15;'

q_materialfreq = 'SELECT a.material, count(a.material) as c FROM artworks a GROUP BY a.material ORDER BY c DESC LIMIT 15;'

q_titlebymater = 'SELECT a.material, a.artwork_title, count(a.artist_id) as c FROM artworks a GROUP BY a.material, a.artwork_title ORDER BY c DESC LIMIT 25;'

q_titlebymaterbyartist = 'SELECT a.material, a.artwork_title, ar.artist, count(a.artist_id) as c FROM artworks a, artists ar WHERE a.artist_id = ar.id GROUP BY a.material, a.artwork_title, ar.artist ORDER BY c DESC LIMIT 25;'
 

conn = sqlite3.connect('../data/db/entartete_kunst.db')
c = conn.cursor()


def run_query(q):
  for row in c.execute(q):
    print "%s | %s | %s | %s" % (row[0], (row[1] if len(row) > 1 else 'end'), (row[2] if len(row) > 2 else 'end'), (row[3] if len(row) > 3 else 'end'))




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

print 'average age at exhib - (real tenuous)======='
run_query(q_avgage)

print 'most frequent subject terms ====='
run_query(q_freqsterms)

print 'commanders of the cross subject term ====='
run_query(q_cmderx)

print 'most frequent titles ====='
run_query(q_titlefreq)

print 'most frequent materials or techniques ====='
run_query(q_materialfreq)

print 'titles by material======='
run_query(q_titlebymaterbyartist)
