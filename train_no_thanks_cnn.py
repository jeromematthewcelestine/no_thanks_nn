from no_thanks import NoThanksGame, NoThanksState
from no_thanks_dataset import NoThanksDataset
from minimax import Minimaxer
from torch.utils.data import DataLoader
import torch
from torch import nn
from no_thanks_nn import NoThanksNN

import torch
from torch.utils.tensorboard import SummaryWriter
writer = SummaryWriter()

params_20240218_01 = {
   'lr': 5e-3,
    'batch_size': 256,
    'epochs': 5000,
    'n_hidden': 100
}
params_20240219_03 = {
    'lr': 5e-3,
    'batch_size': 1000,
    'epochs': 6000,
    'n_hidden': 100
}

params = params_20240219_03

loss_fn = nn.MSELoss()



if __name__ == '__main__':
  train_dataloader = DataLoader(NoThanksDataset('2024-02-18_no_thanks_training_data_03_train.csv'), batch_size=params['batch_size'], shuffle=True)
  test_dataloader = DataLoader(NoThanksDataset('2024-02-18_no_thanks_training_data_03_test.csv'), batch_size=params['batch_size'], shuffle=True)

  # Display image and label.
  train_features, train_labels = next(iter(train_dataloader))

  print(f"Feature batch shape: {train_features.size()}")
  print(f"Labels batch shape: {train_labels.size()}")
  # img = train_features[0].squeeze()
  print(train_features)
  label = train_labels[0]
  print(f"Label: {label}")

  # # device = torch.device('mps' if torch.backends.mps.is_available() else 'cpu')
  # # print(f"Using device {device}")

  model = NoThanksNN(params['n_hidden'])
  print(model)

  input = torch.rand(params['batch_size'], 24)
  output = model(input)
  print(f"Predicted output: {output}")
  print(f"Predicted output shape: {output.size()}")

  optimizer = torch.optim.SGD(model.parameters(), lr=params['lr'])

  test_num_batches = len(test_dataloader)
  train_num_batches = len(train_dataloader)

  for t in range(params['epochs']):
    
    print(f"Epoch {t+1}\n-------------------------------")

    model.train()

    train_loss = 0.0
    for batch, (X, y) in enumerate(train_dataloader):
      pred = model(X)
      loss = loss_fn(pred, y)
      
      optimizer.zero_grad()
      loss.backward()
      optimizer.step()

      with torch.no_grad():
        train_loss += loss.item()

    model.eval()
    
    test_loss, correct = 0, 0

      # Evaluating the model with torch.no_grad() ensures that no gradients are computed during test mode
      # also serves to reduce unnecessary gradient computations and memory usage for tensors with requires_grad=True
    with torch.no_grad():
      for X, y in test_dataloader:
        pred = model(X)
        test_loss += loss_fn(pred, y).item()
    
    train_loss /= train_num_batches
    test_loss /= test_num_batches
    
    print(f"Train loss: {loss:>7f}")
    print(f"Test loss : {(test_loss):>7f}")
    writer.add_scalar("Loss/train", train_loss, t)
    writer.add_scalar("Loss/test", test_loss, t)

    writer.flush()


torch.save(model.state_dict(), f'2024-02-19_no_thanks_nn_03.pth')

  
