#!/usr/bin/env python

import pymongo                                  # python mongo driver
import csv                                      # support for reading and writing csv files
import numpy as np                              # python numerical analyisis package

###################################################################################
###########          Start Global Definitions                          ############
###################################################################################

# start up a mongodb client on port 27017
client = pymongo.MongoClient('mongodb://localhost:27017')

# get the test database
db = client.test

# globals for testing
SEED_WRITE_VOLUME = 1000                # how many documents should you start with?
BURST_WRITE_INTERVAL = 200              # how long between each write burst?
BURST_WRITE_VOLUME = 1000               # how many additional documents per write burst?

BURST_WRITE_PERCENT = 1                 # scaling percent writes

TEST_ITERS = 1000                       # how many cycles do you want?

RECORD_GRANULARITY = 5                  # how many finds between each granular test

# define arErr function for average relative error calculation
def arErr(testSet, hist, truth):
    errVal = 0
    nInc = 0
    for query in testSet:
        # estimate result using histogram
        est = 0;
        [lo, hi] = query
        
        val = np.sum((truth >= lo) & (truth < hi))

        for [hlo, hhi, hval] in hist:
            est = est + ( max(0, (min(hhi, hi) - max(hlo, lo)))/(hhi - hlo))*hval
        # calculate relative error
        if (val != 0):
            errVal = errVal + (abs(val - est) / val)
            nInc = nInc + 1

    if nInc > 0:
        errVal = errVal / nInc
    return errVal


###################################################################################
###########          Start Simulation Run                              ############
###################################################################################

nIt = 0;

testRaw = [line.split(',') for line in open('data/test.in')]
testRaw = [[float(i) for i in k] for k in testRaw]

testRanges = np.array(testRaw)
testRanges = testRanges[:,0:2]

trainRaw = [line.split(',') for line in open('data/gen.in')]
trainRaw = [[float(i) for i in k] for k in trainRaw]

trainRanges = np.array(trainRaw)
trainRanges = trainRanges[:,0:2]

truth = np.array([])

scores = []

# build an index on "a"
db.test.ensure_index('a')

with open('data/gen.truth', 'rb') as truthFile:
    # seed with initial data
    for i in range(0, SEED_WRITE_VOLUME):
        val = truthFile.next()
        val = float(val)
        print "SEED [{}]".format(val)
        db.test.insert( { "a" : val } )
        truth = np.append(truth, [val])

    # start training
    nIt = 0;
    for [lowBound, highBound] in trainRanges:
        nIt += 1
        print "Training Iteration : {}" .format(nIt)
        
        if nIt >= TEST_ITERS:
            break

        if nIt % BURST_WRITE_INTERVAL == 0:
            for i in range(0, BURST_WRITE_PERCENT * len(truth)):
                val = truthFile.next()
                val = float(val)
                print "BURST [{}]".format(val)
                db.test.insert( { "a" : val } )
                truth = np.append(truth, [val])

        # update histogram
        it = db.test.find( {'a' : {"$gte" : lowBound, "$lt" : highBound } } )   # train 
        m = list(it)            # blocking operation
 
        # test histogram
        hist = [line.split(',') for line in open('/data/db/debug.log')]
        hist = [[float(i) for i in line] for line in hist]
        
        val = arErr(testRanges, hist, truth)
        #print val
        scores.append(val)


# print out everything 
with open ('out/arErr.out', 'w') as outFile:
    for score in scores:
            print>>outFile, score


with open ('data/gen.truth', 'w') as outFile:
    for val in truth:
            print>>outFile, val


