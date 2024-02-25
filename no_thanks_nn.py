import torch
from torch import nn

class NoThanksNN(nn.Module):
  def __init__(self, n_hidden):
      super().__init__()
      self.n_hidden = n_hidden
      self.flatten = nn.Flatten()
      self.linear_relu_stack = nn.Sequential(
          nn.Linear(24, n_hidden),
          nn.ReLU(),
          nn.Linear(n_hidden, n_hidden),
          nn.ReLU(),
          nn.Linear(n_hidden, 1),
          nn.ReLU()
      )
 
  def forward(self, x):
      x = self.flatten(x)
      x = self.linear_relu_stack(x)
      return x