import preproc
import model
import data
import tensorflow as tf
from keras.backend.tensorflow_backend import set_session
from keras.callbacks import TensorBoard

#
# config = tf.ConfigProto()
# config.gpu_options.per_process_gpu_memory_fraction = 0.1
# set_session(tf.Session(config=config))

X_train, Y_train, X_test, Y_test = data.get_train_test()
print (X_train.shape)
print (Y_train.shape)
print (X_test.shape)
print (Y_test.shape)

model = model.get_model(TAG = 'best')

print(model.summary())
callbacks = [
    TensorBoard(log_dir='./logs/run_raw', histogram_freq=0, batch_size=32,
                write_graph=True, write_grads=False, write_images=False,
                embeddings_freq=0, embeddings_layer_names=None, embeddings_metadata=None),
]
model.fit(X_train, Y_train, nb_epoch=1000, batch_size=512, validation_data=(X_test, Y_test), callbacks=callbacks)
# Final evaluation of the model
scores = model.evaluate(X_test, Y_test, verbose=0)
print("Accuracy: %.2f%%" % (scores[1] * 100))
model.save("model_default.model")
