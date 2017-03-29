# coding: utf-8
import os
import pickle
from storage.model import TrajectoryRoadTriple


array = []
array.append(TrajectoryRoadTriple("111", "123", "123"))
array.append(TrajectoryRoadTriple("222", "123", "123"))

f = open('test', 'wb')
pickle.dump(array, f)
f.close()



# Load data
f2 = open('test', 'rb')
data = pickle.load(f2)
for line in data:
    print line.road_id