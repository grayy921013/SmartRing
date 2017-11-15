#!/usr/local/bin/python2
import numpy as np
from sklearn import preprocessing as pre

X = np.load('X_train.npy')
X_abs_scale = [pre.minmax_scale(x) for x in X]
X_test = np.load('X_test.npy')
X_test_abs_scale = [pre.minmax_scale(x) for x in X_test]
np.save('X_train.max-min-abs-scale.npy', X_abs_scale)
np.save('X_test.max-min-abs-scale.npy', X_test_abs_scale)

