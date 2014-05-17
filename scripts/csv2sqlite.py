#!/usr/bin/env python


import sqlite3
import csv

conn = sqlite3.connect('../data/db/entartete_kunst.db')
c = conn.cursor()


def import_table():
  c.execute("CREATE TABLE artworks (catalog_id, db_id, loss_thru, artwork_title, location, date_lost, material, ek_inven_id, uri, art_form, envelope, work_status, db_title, work_date, artist_id, copyright, inv_orig, env_part, thumb_url, museum_orig);")
  with open('../data/apr-2014/degenerate_artists_work.csv', 'rb') as file:
    dr = csv.DictReader(file)
    next(dr)
    to_db = [(unicode(i['catalog_id'], "utf8"),
              unicode(i['db_id'], "utf8"),
              unicode(i['loss_thru'], "utf8"),
              unicode(i['artwork_title'], "utf8"),
              unicode(i['location'], "utf8"),
              unicode(i['date_lost'], "utf8"),
              unicode(i['material'], "utf8"),
              unicode(i['ek_inven_id'], "utf8"),
              unicode(i['uri'], "utf8"),
              unicode(i['art_form'], "utf8"),
              unicode(i['envelope'], "utf8"),
              unicode(i['work_status'], "utf8"),
              unicode(i['db_title'], "utf8"),
              unicode(i['work_date'], "utf8"),
              unicode(i['artist_id'], "utf8"),
              unicode(i['copyright'], "utf8"),
              unicode(i['inv_orig'], "utf8"),
              unicode(i['env_part'], "utf8"),
              unicode(i['thumb_url'], "utf8"),
              unicode(i['museum_orig'], "utf8")) for i in dr]

  c.executemany("INSERT INTO artworks (catalog_id, db_id, loss_thru, artwork_title, location, date_lost, material, ek_inven_id, uri, art_form, envelope, work_status, db_title, work_date, artist_id, copyright, inv_orig, env_part, thumb_url, museum_orig) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", to_db)

  conn.commit()

def import_move():
  c.execute("CREATE TABLE movements (id, mvmnt);")
  with open('../data/db/artists-movements.csv', 'rb') as file:
    dr = csv.DictReader(file)
    next(dr)
    to_db = [(unicode(i['id'], "utf8"),
              unicode(i['mvmnt'], "utf8")
              ) for i in dr]

  c.executemany("INSERT INTO movements (id, mvmnt) VALUES (?, ?);", to_db)

  conn.commit()


#import_table()
import_move()
