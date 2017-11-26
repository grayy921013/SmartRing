import model as m
import data
import tensorflow as tf
from keras.backend.tensorflow_backend import set_session
from keras.callbacks import TensorBoard, EarlyStopping
import sys
import config
from datetime import datetime
#
# config = tf.ConfigProto()
# config.gpu_options.per_process_gpu_memory_fraction = 0.1
# set_session(tf.Session(config=config))

data_mode = "raw"
print(sys.argv)
if len(sys.argv) > 1:
    data_mode = sys.argv[1]

X_train, Y_train, X_test, Y_test = data.get_calibrate_data_npy()

# data augmentation via adding noises
# X_train, Y_train = data.add_noise(X_train, Y_train)

name = data_mode + "_calibrate" + "_" + str(datetime.now())

model = m.calibrate_rnn()

print(model.summary())
callbacks = [
]

config = tf.ConfigProto()
config.gpu_options.allow_growth = True
sess = tf.Session(config=config)
tf.global_variables_initializer().run(session=sess)

model.fit(X_train, Y_train, nb_epoch=300, batch_size=64, validation_data=(X_test, Y_test), callbacks=callbacks)
# Final evaluation of the model
scores = model.evaluate(X_test, Y_test, verbose=0)
model.save('model_' + name + ".model")
f = open("log", "a+")
f.write(name + " Accuracy: %.2f%%" % (scores[1]*100))
f.write("\n")
f.close()
