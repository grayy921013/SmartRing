import preproc
import model
import tensorflow as tf
from keras.backend.tensorflow_backend import set_session

config = tf.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.1
set_session(tf.Session(config=config))

X_train, Y_train, X_test, Y_test = preproc.get_train_test()
model = model.get_model()

print(model.summary())
model.fit(X_train, Y_train, nb_epoch=1000, batch_size=64)
# Final evaluation of the model
scores = model.evaluate(X_test, Y_test, verbose=0)
print("Accuracy: %.2f%%" % (scores[1]*100))