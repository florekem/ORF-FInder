import numpy as np
import h5py


with h5py.File('sequences.hdf5', 'r') as f:
     print(list(f.items()))
