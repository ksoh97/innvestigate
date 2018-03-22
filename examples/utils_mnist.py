import numpy as np

import keras
from keras.datasets import mnist
from keras.models import Model
from keras.layers import Dense, Dropout, Activation, Input
from keras.optimizers import RMSprop, Adam

import innvestigate
import innvestigate.utils as iutils
import innvestigate.utils.visualizations as ivis


def fetch_data(channels_first):
    # the data, shuffled and split between train and test sets
    (x_train, y_train), (x_test, y_test) = mnist.load_data()

    if channels_first:
        x_train = x_train.reshape(60000, 1, 28, 28)
        x_test = x_test.reshape(10000, 1, 28, 28)
    else:
        x_train = x_train.reshape(60000, 28, 28, 1)
        x_test = x_test.reshape(10000, 28, 28, 1)
    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')
    print(x_train.shape[0], 'train samples')
    print(x_test.shape[0], 'test samples')

    return x_train, y_train, x_test, y_test


def preprocess(X, zero_mean):
    X.copy()
    X /= 255
    if zero_mean:
        X -= 0.5
    return X


def create_model(channels_first, activation, num_classes, dense_units=1024, dropout_rate=0.25):
    if channels_first:
        input_shape = (None, 1, 28, 28)
    else:
        input_shape = (None, 28, 28, 1)

    network = innvestigate.utils.tests.networks.base.mlp_2dense(
        input_shape,
        num_classes,
		activation = activation,
        dense_units = dense_units,
        dropout_rate = dropout_rate)
    model_wo_sm = Model(inputs=network["in"], outputs=network["out"])
    model_w_sm = Model(inputs=network["in"], outputs=network["sm_out"])
    return model_wo_sm, model_w_sm


def train_model(model, data, batch_size=128, epochs=20):
    num_classes = 10

    x_train, y_train, x_test, y_test = data
    # convert class vectors to binary class matrices
    y_train = keras.utils.to_categorical(y_train, num_classes)
    y_test = keras.utils.to_categorical(y_test, num_classes)

    model.compile(loss='categorical_crossentropy',
                  optimizer=Adam(),
                  metrics=['accuracy'])

    history = model.fit(x_train, y_train,
                        batch_size=batch_size,
                        epochs=epochs,
                        verbose=1)
    score = model.evaluate(x_test, y_test, verbose=0)
    print('Test loss:', score[0])
    print('Test accuracy:', score[1])
    pass

# Utility function.

def postprocess(X):
    X = X.copy()
    X = iutils.postprocess_images(X)
    return X

def image(X):
    X = X.copy()
    X = iutils.postprocess_images(X)
    return ivis.graymap(X,
                        input_is_postive_only=True)

def bk_proj(X):
    return ivis.graymap(X)

def heatmap(X):
    return ivis.heatmap(X)

def graymap(X):
    return ivis.graymap(np.abs(X), input_is_postive_only=True)