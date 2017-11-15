#!/usr/local/bin/python2
import numpy as np
from sklearn import preprocessing as pre

#
# this script is for generating preprocessed data
#

def gen_scale_data():
    X = np.load('X_train.npy')
    X_abs_scale = [pre.minmax_scale(x) for x in X]
    X_test = np.load('X_test.npy')
    X_test_abs_scale = [pre.minmax_scale(x) for x in X_test]
    np.save('X_train.max-min-abs-scale.npy', X_abs_scale)
    np.save('X_test.max-min-abs-scale.npy', X_test_abs_scale)
    print ('gen_scale_data done')


def gen_rounding_data():
    X_train = np.load('X_train.npy')
    X_test = np.load('X_test.npy')
    np.save('X_train_rounded', X_train // 100)
    np.save('X_test_rounded', X_test // 100)
    print ('gen_rounding_data done')


if __name__ == '__main__':
    gen_scale_data()
    gen_rounding_data()