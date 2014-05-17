#!/usr/bin/env python

import csv

import time
from datetime import datetime

'''This scripts purpose is to input a csv file of a specific structure
and output individual tables (csv files themselves) for each column that is a comma separated list of entities'''


fname1 = '../data/artists-movements-'+datetime.now().isoformat()+'.csv'
fname2 = '../data/artists-nations-'+datetime.now().isoformat()+'.csv'
fname3 = '../data/artists-sterms-'+datetime.now().isoformat()+'.csv'

with open('../data/artists-full-2014-05-17.csv', 'r') as file:
  r = csv.reader(file)
  w_mvmnt = csv.writer(open(fname1, 'w'))
  w_nation = csv.writer(open(fname2, 'w'))
  w_sterms = csv.writer(open(fname3, 'w'))

  next(r) #skip header

  header1 = ['id', 'mvmnt']
  header2 = ['id', 'nation']
  header3 = ['id', 'subject']

  w_mvmnt.writerow(header1)
  w_nation.writerow(header2)
  w_sterms.writerow(header3)


  for row in r:

    #movement
    mvmnt = row[4].split(',')
    for s in mvmnt:
      w_mvmnt.writerow([row[0], s.strip()])

    #nationality
    nation = row[3].split(',')
    for s in nation:
      w_nation.writerow([row[0], s.strip()])

    #subject terms
    sterms = row[7].split(',')
    for s in sterms:
      w_sterms.writerow([row[0], s.strip()])
