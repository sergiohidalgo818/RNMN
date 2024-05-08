import numpy as np
from keras.api.utils import text_dataset_from_directory
from keras import layers
import keras
from keras.api.models import Model
import tensorflow
import re
import string

def vectorize_text(text, label):
        text = tensorflow.expand_dims(text, -1)
        return vectorize_layer(text), label
    
    
def custom_standardization(input_data):
        lowercase = tensorflow.strings.lower(input_data)
        return tensorflow.strings.regex_replace(
            lowercase, f"[{re.escape(string.punctuation)}]", ""
    )

array_x: np.ndarray
array_y: np.ndarray
batch_size = 32

raw_train_ds = text_dataset_from_directory(directory="data/text_data/train",label_mode="categorical",
                        batch_size=batch_size,
                        validation_split=0.2,
                        subset="training", seed=1337, labels='inferred')

raw_test_ds = text_dataset_from_directory(
                        directory="data/text_data/test",label_mode="categorical",
                        batch_size=batch_size,  labels='inferred')




text_ds = raw_train_ds.map(lambda x, y: x)


max_features = 20000
embedding_dim = 128
sequence_length = 500

vectorize_layer = layers.TextVectorization(
standardize=custom_standardization,
max_tokens=max_features,
output_mode="int",
output_sequence_length=sequence_length,
)

vectorize_layer.adapt(text_ds)

train_ds = raw_train_ds.map(vectorize_text)
test_ds = raw_test_ds.map(vectorize_text)

inlayer = layers.Input(shape=(None,), dtype="int64")
aux_layer = layers.Embedding(max_features, embedding_dim)(inlayer)
aux_layer = layers.Dropout(0.5)(aux_layer)
aux_layer = layers.Conv1D(128, 7, padding="valid", activation="relu", strides=3)(aux_layer)
aux_layer = layers.Conv1D(128, 7, padding="valid", activation="relu", strides=3)(aux_layer)
aux_layer = layers.GlobalMaxPooling1D()(aux_layer)
aux_layer = layers.Dense(128, activation="relu")(aux_layer)
aux_layer = layers.Dropout(0.5)(aux_layer)
aux_layer = layers.Dense(10, activation="softmax")(aux_layer)

model = Model(inputs=inlayer, outputs=aux_layer)

model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])

epochs = 3


history = model.fit(train_ds, validation_data=test_ds, epochs=epochs)

# A string input
inputs = keras.Input(shape=(1,), dtype="string")
# Turn strings into vocab indices
indices = vectorize_layer(inputs)
# Turn vocab indices into predictions
outputs = model(indices)

# Our end to end model
end_to_end_model = keras.Model(inputs, outputs)
end_to_end_model.compile(
    loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"]
)
# Test it with `raw_test_ds`, which yields raw strings

nums = ['cero', 'uno', 'dos', 'tres', 'cuatro',
            'cinco', 'seis', 'siete', 'ocho', 'nueve']
numpydata = tensorflow.convert_to_tensor(nums, dtype="string")
array = end_to_end_model.predict(numpydata)

for i in range (array.shape[0]):
    print(np.argmax(array[i]))
