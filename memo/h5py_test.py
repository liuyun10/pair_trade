import numpy as np
import h5py

f = h5py.File('file_open_sample.hdf5')
# ...必要な処理を記述。
# 終わったらcloseメソッドで閉じます。
f.close()