import preproc
import model
import data
import tensorflow as tf
from keras.backend.tensorflow_backend import set_session
from keras.callbacks import TensorBoard
import sys

#
# config = tf.ConfigProto()
# config.gpu_options.per_process_gpu_memory_fraction = 0.1
# set_session(tf.Session(config=config))

print(sys.argv)
X_train, Y_train, X_test, Y_test = data.get_data(sys.argv[1])
hps = [4, 0.2, 100, 0.2]
name = sys.argv[1] + "_" + '_'.join(str(x) for x in hps)
for i in range(2, len(sys.argv)):
    if i % 2 == 0:
        hps[i - 2] = int(sys.argv[i])
    else:
        hps[i - 2] = float(sys.argv[i])

print("hyperparameters: " + str(hps))
model = model.get_model(hps)

print(model.summary())
callbacks = [
    TensorBoard(log_dir='./logs/' + name, histogram_freq=0, batch_size=32,
                write_graph=True, write_grads=False, write_images=False,
                embeddings_freq=0, embeddings_layer_names=None, embeddings_metadata=None),
]
model.fit(X_train, Y_train, nb_epoch=1000, batch_size=512, validation_data=(X_test, Y_test), callbacks=callbacks)
# Final evaluation of the model
scores = model.evaluate(X_test, Y_test, verbose=0)
model.save('model_' + name + ".model")
f = open("log", "a+")
f.write(name + " Accuracy: %.2f%%" % (scores[1]*100))
f.write("\n")
f.close()