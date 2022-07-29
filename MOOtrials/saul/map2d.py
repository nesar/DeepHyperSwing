import time
import numpy as np
from deephyper.problem import HpProblem
from deephyper.evaluator import profile
import gzip
import matplotlib.pyplot as plt
import tensorflow as tf
from data.utils import load_data, load_data_prepared
from sklearn.decomposition import PCA
from deephyper.nas.metrics import r2
from keras.utils.layer_utils import count_params



problem = HpProblem()
problem.add_hyperparameter(["sigmoid", "tanh", "relu"], "activation", default_value="relu")
problem.add_hyperparameter((1e-5, 1e-2, "log-uniform"), "learning_rate", default_value=1e-3)
problem.add_hyperparameter((1, 4), "batch_size", default_value=4)
problem.add_hyperparameter((4, 20), "epochs", default_value=10)

from common import RUN_SLEEP


def basic_sleep():
    time.sleep(RUN_SLEEP)


def cpu_bound():
    t = time.time()
    duration = 0
    while duration < RUN_SLEEP:
        sum(i * i for i in range(10**7))
        duration = time.time() - t


def IO_bound():
    with open("/dev/urandom", "rb") as f:
        t = time.time()
        duration = 0
        while duration < RUN_SLEEP:
            f.read(100)
            duration = time.time() - t


def build_and_train_model(config: dict, n_components: int = 2, verbose: bool = 0):
    '''
    Function with loading data, model config, training routine
    to test: 
    model, history = build_and_train_model(config={}, verbose=1)
    '''
    tf.keras.utils.set_random_seed(42)

    default_config = {
        "activation": "relu",
        "learning_rate": 1e-3,
        "batch_size": 4,
        "epochs": 5,
    }
    default_config.update(config)
    
    nSamples = 1000
    nGrid = 1024
    train_test_split = 0.9

    
    (X_train, y_train), (X_valid, y_valid) = load_data_prepared(nSamples, nGrid, train_test_split)


    model = tf.keras.Sequential(
        [tf.keras.Input(shape=X_train.shape[1:])] 
        + [tf.keras.layers.Conv2D(128, kernel_size=3, activation='relu', strides=2, padding='same')]
        + [tf.keras.layers.Conv2D(64, kernel_size=3, activation='relu', strides=2, padding='same')]
        + [tf.keras.layers.Conv2D(64, kernel_size=3, activation='relu', strides=4, padding='same')]
        + [tf.keras.layers.Conv2D(64, kernel_size=3, activation='relu', strides=4, padding='same')]
        + [tf.keras.layers.Conv2D(64, kernel_size=3, activation='relu', strides=4, padding='same')]
        + [tf.keras.layers.Flatten()]
        # + layers
        + [tf.keras.layers.Dense(512**n_components, activation=default_config["activation"])]
        + [tf.keras.layers.Dense(64*n_components, activation=default_config["activation"])]
        + [tf.keras.layers.Dense(32*n_components, activation=default_config["activation"])]
        + [tf.keras.layers.Dense(n_components, activation='linear')]
    )
    


    if verbose:
        model.summary()
        
        
    def metric1(y_true, y_pred):
        squared_difference = tf.square(y_true - y_pred)
        return tf.reduce_mean(squared_difference, axis=0)[0]


    def metric2(y_true, y_pred):
        squared_difference = tf.square(y_true - y_pred)
        return tf.reduce_mean(squared_difference, axis=0)[1]


    optimizer = tf.keras.optimizers.Adam(learning_rate=default_config["learning_rate"])
    model.compile(optimizer, "mse", metrics=[metric1, metric2])

    history = model.fit(
        X_train,
        y_train,
        epochs=default_config["epochs"],
        batch_size=default_config["batch_size"],
        validation_data=(X_valid, y_valid),
        verbose=verbose,
    ).history

    return model, history



@profile
def run(config):
    # important to avoid memory exploision
    tf.keras.backend.clear_session()
    model, history = build_and_train_model(config, verbose=0)
    # return -history["val_loss"][-1], -count_params(model.trainable_weights)
    return -history["val_metric1"][-1], -history["val_metric2"][-1]
