from matplotlib.pyplot import axis
import numpy as np
from random import shuffle

def softmax_loss_naive(W, X, y, reg):
    """
    Softmax loss function, naive implementation (with loops)
    
    Inputs have dimension D, there are C classes, and we operate on minibatches
    of N examples.
    
    Inputs:
    - W: A numpy array of shape (D, C) containing weights.
    - X: A numpy array of shape (N, D) containing a minibatch of data.
    - y: A numpy array of shape (N,) containing training labels; y[i] = c means
      that X[i] has label c, where 0 <= c < C.
    - reg: (float) regularization strength
    
    Returns a tuple of:
    - loss as single float
    - gradient with respect to weights W; an array of same shape as W
    """
    # Initialize the loss and gradient to zero.
    loss = 0.0
    dW = np.zeros_like(W)

    #############################################################################
    # TODO: Compute the softmax loss and its gradient using explicit loops.     #
    # Store the loss in loss and the gradient in dW. If you are not careful     #
    # here, it is easy to run into numeric instability. Don't forget the        #
    # regularization!                                                           #
    #############################################################################
    num_classes = W.shape[1]
    num_train = X.shape[0]

    scores = np.dot(X, W)
    scores -= np.max(scores, axis = 1).reshape(num_train, 1)

    for i in range(num_train):
        loss += -np.log(np.exp(scores[i, y[i]]) / np.sum(np.exp(scores[i])))
        dW[:, y[i]] += (np.exp(scores[i, y[i]]) / np.sum(np.exp(scores[i])) - 1) * X[i]
        
        for j in range(num_classes):
            if j == y[i]:
                continue
            dW[:, j] += (np.exp(scores[i, j]) / np.sum(np.exp(scores[i]))) * X[i]
    
    loss /= num_train
    loss += 0.5 * reg * np.sum(W ** 2)
    
    dW /= num_train
    dW += reg * W
            

    #############################################################################
    #                          END OF YOUR CODE                                 #
    #############################################################################
    
    return loss, dW


def softmax_loss_vectorized(W, X, y, reg):
    """
    Softmax loss function, vectorized version.
    
    Inputs and outputs are the same as softmax_loss_naive.
    """
    # Initialize the loss and gradient to zero.
    loss = 0.0
    dW = np.zeros_like(W)
    
    #############################################################################
    # TODO: Compute the softmax loss and its gradient using no explicit loops.  #
    # Store the loss in loss and the gradient in dW. If you are not careful     #
    # here, it is easy to run into numeric instability. Don't forget the        #
    # regularization!                                                           #
    #############################################################################
    num_train = X.shape[0]

    scores = np.dot(X,W)
    scores -= np.max(scores, axis = 1).reshape(num_train, 1)
    norm_scores = np.exp(scores) / np.sum(np.exp(scores), axis = 1).reshape(num_train, 1)
    
    loss = -np.sum(np.log(norm_scores[np.arange(num_train), y]))
    loss /= num_train
    loss += 0.5 * reg * np.sum(W * W)

    norm_scores[np.arange(num_train), y] -= 1
    
    dW = np.dot(X.T, norm_scores)
    dW /= num_train
    dW += reg * W

    #############################################################################
    #                          END OF YOUR CODE                                 #
    #############################################################################
    
    return loss, dW
