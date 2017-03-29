# coding: utf-8
import os
import hickle as hkl
import numpy as np
from storage.model import TrajectoryRoadTriple


array = []
array.append(TrajectoryRoadTriple("111", "123", "123"))
array.append(TrajectoryRoadTriple("222", "123", "123"))

np_array = np.array(array)

# Dump to file
hkl.dump(np_array, 'test.hkl', mode='w')



# Load data
array_hkl = hkl.load('test.hkl')

for line in array:
    print line.road_id
