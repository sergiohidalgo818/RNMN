import numpy as np
import os
from keras.api.utils import text_dataset_from_directory

directory = os.path.join("data", "text_data")
(x_train, y_train) = (np.array([]), np.array([]))
(x_test, y_test) = (np.array([]), np.array([]))

directory_train = os.path.join(directory, "train")
batch_size = 32

raw_train_ds = text_dataset_from_directory(
                        directory=directory_train,
                        batch_size=batch_size,
                        validation_split=0.2,
                        subset="training", seed=1337, labels='inferred')
raw_test_ds = text_dataset_from_directory(
                        directory=directory_train,
                        batch_size=batch_size,  labels='inferred')

for text_batch, label_batch in raw_train_ds.take(1):
    for i in range(10):
        print(text_batch.numpy()[i])
        print(label_batch.numpy()[i])
