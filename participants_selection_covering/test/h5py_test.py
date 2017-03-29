# coding: utf-8
import os
import h5py
import numpy as np

f = h5py.File("mytestfile.hdf5", "w")
dset = f.create_dataset("mydataset", (100,), dtype='i')
print dset.shape
print dset.dtype
print dset.name
print f.name
grp = f.create_group("subgroup")
print grp.name
dset2 = grp.create_dataset("another_dataset", (50,), dtype='f')
print dset2.name

for name in f:
    print name

