#!/usr/bin/env python

import pymongo                  # python mongo driver
import csv                      # support for reading and writing csv files
import numpy                    # python numerical analyisis package

# define arErr function for average relative error calculation
def arErr(testSet, hist):
    errVal = 0
    nInc = 0
    for query in testSet:
        # estimate result using histogram
        est = 0;
        [lo, hi, val] = query
        for [hlo, hhi, hval] in hist:
            est = est + ( max(0, (min(hhi, hi) - max(hlo, lo)))/(hhi - hlo))*hval
        # calculate relative error
        if (val != 0):
            errVal = errVal + (abs(val - est) / val)
            nInc = nInc + 1
    errVal = errVal / nInc
    return errVal




