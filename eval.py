import config
import data
from keras.models import load_model
import numpy as np

model_name = 'model_default.model'

x_test = data.get_from_test_folder()

model = load_model(model_name)
res = model.predict_classes(x_test[0], batch_size=config.batch_size, verbose=0)
print (res[0])