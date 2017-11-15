from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
import numpy
from keras.callbacks import TensorBoard

max_review_length = 200
X_train = numpy.load('X_train.npy')
X_test = numpy.load('X_test.npy')
Y_train = numpy.load('Y_train.npy')
Y_test = numpy.load('Y_test.npy')
model = Sequential()
model.add(LSTM(output_dim=4, input_shape=(max_review_length, 6), return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(100))
model.add(Dropout(0.2))
model.add(Dense(10, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
print(model.summary())
callbacks = [
    TensorBoard(log_dir='./logs/run_raw', histogram_freq=0, batch_size=32, write_graph=True, write_grads=False, write_images=False, embeddings_freq=0, embeddings_layer_names=None, embeddings_metadata=None),
]
model.fit(X_train, Y_train, nb_epoch=1000, batch_size=512, validation_data=(X_test, Y_test), callbacks=callbacks)
# Final evaluation of the model
scores = model.evaluate(X_test, Y_test, verbose=0)
print("Accuracy: %.2f%%" % (scores[1]*100))