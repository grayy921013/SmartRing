import numpy

X_train = numpy.load('X_train.npy')
X_test = numpy.load('X_test.npy')
numpy.save('X_train_rounded', X_train//100)
numpy.save('X_test_rounded', X_test//100)