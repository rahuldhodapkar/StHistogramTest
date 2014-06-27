#!/usr/bin/env python

import pymongo                                  # python mongo driver
import csv                                      # support for reading and writing csv files
import numpy                                    # python numerical analyisis package
from db_simulation_harness import arErr         # custom testing harness

###################################################################################
###########          Start Global Definitions                          ############
###################################################################################

# start up a mongodb client on port 27017
client = pymongo.MongoClient('mongodb://localhost:27017')

# get the test database
db = client.test

###################################################################################
###########          Start Simulation Run                              ############
###################################################################################

with open('data/gen.truth', 'rb') as truthFile:
    for line in truthFile:
        val = float(line)
        print "inserting {}" .format(val)
        db.test.insert( { "a" : val } )                      # insert into database

# build an index on "a"
db.test.ensure_index('a')

# construct the test dataset
testSet = [line.split(',') for line in open('data/test.in')]
testSet = [[float(i) for i in k] for k in testSet]

scores = []                     # init scores array
# train database on a set of queries
with open('data/gen.in', 'rb') as trainingQueries:
    reader = csv.reader(trainingQueries, delimiter=',')
    nIter = 0
    for row in reader:
        if (nIter > 1000):
            break
        nIter = nIter + 1
        print "( {} -> {} = {} )".format(row[0], row[1], row[2])
        it = db.test.find( {'a' : {"$gte" : float(row[0]), "$lt" : float(row[1])} } )   # train 
        m = list(it)            # blocking operation
        
        # pull most recent histogram output.
        # run convergence analysis here.
        hist = [line.split(',') for line in open('/data/db/debug.log')]
        hist = [[float(i) for i in line] for line in hist]
        # print hist
        val = arErr(testSet, hist)
        print val
        scores.append(val)

# now write out scores to file
with open('out/arErr.out', 'w') as outFile:
    for score in scores:
        print>>outFile, score

# run convergence analyses: "average relative error"

# with open('../data/gen.in', 'rb') as genFile:
#    reader = csv.reader(genFile, delimiter=",")
#    for row in reader:
        # perform a mongodb query.

