from tensorflow.keras.callbacks import Callback
import pandas as pd
import numpy as np


class ModelMetricCallback(Callback):
    """
    Each epoch applies metrics on the entire model. Saves the result in pd.DataFrame under <.results>.
    TODO examples.
    """
    def __init__(self, metrics = {}):
        self.metrics = metrics
        self.results = {}
        

    def on_epoch_end(self, epoch, logs={}):
      result = []
      #evaluate model metrics
      for metric in self.metrics.values():
        result.append(metric(self.model))
      self.results[epoch] = result
      

    def on_train_end(self, logs={}):
      self.results = pd.DataFrame.from_dict(self.results, orient='index', columns=list(self.metrics.keys()))
      
      

from tensorflow.keras.callbacks import Callback
import dill as pickle
from pathlib import Path

class WeightSaver(Callback):
  """
  Saves the incoming weights of neurons given by coordinates for each batch with differing step.
  Hint - First layer is the input layer.
  """

  def __init__(self, steps, neurons):
    """Constructor.

    Args:
        steps (Iterable) : How often should be the weights saved for each epoch \
        (last step is used for all following epochs if no more steps are given).

        neurons (Iterable) : Coordinates for each neuron to be followed. First  \
        coordinate gives the layer, second the position in that layer.
    """

    self.steps = steps
    self.step = steps[0]
    self.batch = 0
    self.neurons = neurons
    self.results = [{} for _ in neurons]


  def on_batch_end(self, batch, logs={}):
      if self.batch % self.step == 0:
        # this is to minimize <.get_weights> calls. could be much nicer though.
        layers = {l : self.model.layers[l].get_weights() for l in set([i for i, _ in self.neurons])}
        for i, neuron in enumerate(self.neurons):
          self.results[i][self.batch] = np.swapaxes(layers[neuron[0]][0], 0, 1)[neuron[1]]
      self.batch += 1

  
  def on_epoch_end(self, epoch, logs={}):
    if epoch < len(self.steps):
      self.step = self.steps[epoch]


  def on_train_end(self, logs={}):
    self.results = [pd.DataFrame.from_dict(result, orient='index') for result in self.results]
