from torch.nn import Module, Linear, LSTM
from torch import tensor, double, optim, movedim, no_grad, stack, ones, zeros, float64, long
from torch.nn.functional import relu, mse_loss, sigmoid, cross_entropy, tanh
import pandas as pd


class Network(Module):
    def __init__(self, numFeatures, layers = 50, LR = .005):
        super().__init__()
        ### Implement with your own objects and layers
        self.learningRate = LR
        self.layers = layers
        self.initialLayer = Linear(numFeatures, layers, dtype = float64)
        self.LSTM = LSTM(layers,layers, dtype = float64, batch_first = False)
        self.secondaryLayer = Linear(layers, layers, dtype = float64)
        self.finalLayer = Linear(layers, 2, dtype = float64)
        self.numFeatures = numFeatures
        
    def run(self, input_df):
        '''Input: signalTrail- List of list (maybe tensors) of each channel's signal'''
        ### This is where you put your input through your layers
        # Make Long Term and Short Term Memory Tensors
        x = self.initialLayer(tensor(input_df.to_numpy()))
        x, (hn, cn) = self.LSTM(x)
        #return _
        #print(hn[0].shape)
        x = self.secondaryLayer(hn[-1])
        x = self.finalLayer(relu(x))
        return x
            