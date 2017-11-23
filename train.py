import model
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

X_train, Y_train, X_val, Y_val, X_test, Y_test = data.get_full_data_npy()

# data augmentation via adding noises
# X_train, Y_train = data.add_noise(X_train, Y_train)

hps = [4, 0.5, 100, 0.5]
name = data_mode + "_" + '_'.join(str(x) for x in hps) + "_" + str(datetime.now())
for i in range(2, len(sys.argv)):
    if i % 2 == 0:
        hps[i - 2] = int(sys.argv[i])
    else:
        hps[i - 2] = float(sys.argv[i])

print("hyperparameters: " + str(hps))
model = model.get_model(hps, multiple=True)

print(model.summary())
callbacks = [
    TensorBoard(log_dir='./logs/' + name, histogram_freq=0, batch_size=config.batch_size,
                write_graph=True, write_grads=False, write_images=False,
                embeddings_freq=0, embeddings_layer_names=None, embeddings_metadata=None),
    EarlyStopping(monitor='val_loss',
                  min_delta=0,
                  patience=10,
                  verbose=0, mode='auto'),
]
model.fit(X_train, Y_train, nb_epoch=1000, batch_size=320, validation_data=(X_val, Y_val), callbacks=callbacks)
# Final evaluation of the model
scores = model.evaluate(X_test, Y_test, verbose=0)
model.save('model_' + name + ".model")
f = open("log", "a+")
f.write(name + " Accuracy: %.2f%%" % (scores[1]*100))
f.write("\n")
f.close()
