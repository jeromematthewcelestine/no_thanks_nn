
# Read Me

Using neural networks to solve No Thanks!

## Exercise 01 (2024-02-18)

### No Thanks parameters
* Cards: 1-5, omit 1
* Chips: 1

### NN parameters
* Target: value
* Structure: 24 x 100 -> 100 x 100 -> 100 x 1
* Learning rate: 5e-3
* Batch size: 256
* Loss fn: MSELoss
* Epochs: 5000
* Train on all data -- no test
* Train loss: ~0.15

## Exercise 02 (2024-02-18)

### No Thanks parameters
* Cards: 1-5, omit 1
* Chips: 1

### NN parameters
* Target: value

## Exercise 03 (2024-02-18)

## Exercise 04 (2024-02-19)

* Attempt to overfit a single batch
* Done
* Can get very close to perfect.
* Train loss: ~0.01

## Exercise 03 

* Compare train loss and test loss
* Split (action) data into 75% train, 25% test

### NN parameters
Target: action
Train/test: 75%/25%
Learning rate: 5e-3
Epochs: 6000
Batch size: 1000
Hiden: 100

### Saved model
2024-02-19_no_thanks_nn_03.pth

## Exervise 06 - Decision Tree Model

*



