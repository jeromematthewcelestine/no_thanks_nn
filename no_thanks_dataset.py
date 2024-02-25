import torch
from torch.utils.data import Dataset
import numpy as np

class NoThanksDataset(Dataset):
  def __init__(self, csv_file, transform=None):
    self.data = torch.tensor(np.loadtxt(csv_file, delimiter=','))
    self.transform = transform

  def __len__(self):
    return len(self.data)

  def __getitem__(self, idx):
    sample = self.data[idx]
    state_data = sample[:-1].float()
    value_data = sample[-1].reshape((1)).float()
    if self.transform:
      state_data = self.transform(state_data)
    return state_data, value_data
  
if __name__ == '__main__':
  ds = NoThanksDataset('no_thanks_training_data.csv')
  print(len(ds))
  print(ds[0])