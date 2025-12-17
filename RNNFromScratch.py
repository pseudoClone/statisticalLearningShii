import numpy as np

# --- Data Preparation ---
# For this example, we'll use a simple piece of text.
# In a real-world scenario, you would load this from a file.
data = "hello world. this is a simple rnn example. it is not very smart but it works."
chars = list(set(data))
data_size, vocab_size = len(data), len(chars)
print(f"Data has {data_size} characters, {vocab_size} unique.")

# Create mappings from characters to indices and vice-versa
char_to_ix = {ch: i for i, ch in enumerate(chars)}
ix_to_char = {i: ch for i, ch in enumerate(chars)}

# --- Hyperparameters ---
hidden_size = 100  # Size of the hidden layer of neurons
seq_length = 25    # Number of steps to unroll the RNN for BPTT
learning_rate = 1e-1

# --- RNN Model Definition ---

class RNN:
    def __init__(self, input_size, hidden_size, output_size):
        # Weight matrices
        # Input to hidden
        self.Wxh = np.random.randn(hidden_size, input_size) * 0.01
        # Hidden to hidden (recurrent connection)
        self.Whh = np.random.randn(hidden_size, hidden_size) * 0.01
        # Hidden to output
        self.Why = np.random.randn(output_size, hidden_size) * 0.01

        # Bias vectors
        self.bh = np.zeros((hidden_size, 1))
        self.by = np.zeros((output_size, 1))

    def forward(self, inputs, h_prev):
        """
        Performs the forward pass of the RNN.
        Inputs:
            - inputs: a list of integers (indices of characters)
            - h_prev: previous hidden state
        Returns:
            - xs: inputs stored for backprop
            - hs: hidden states stored for backprop
            - ys: output scores (pre-softmax) stored for backprop
            - ps: probabilities (post-softmax) stored for backprop
            - h: final hidden state
        """
        xs, hs, ys, ps = {}, {}, {}, {}
        h = h_prev
        # Forward pass
        for t in range(len(inputs)):
            # One-hot encode the input character
            xs[t] = np.zeros((vocab_size, 1))
            xs[t][inputs[t]] = 1
            
            # Calculate the new hidden state
            h = np.tanh(np.dot(self.Wxh, xs[t]) + np.dot(self.Whh, h) + self.bh)
            hs[t] = h
            
            # Calculate the output scores (unnormalized log probabilities)
            y = np.dot(self.Why, h) + self.by
            ys[t] = y
            
            # Apply softmax to get probabilities
            ps[t] = np.exp(y) / np.sum(np.exp(y))
            
        return xs, hs, ys, ps, h

    def backward(self, xs, hs, ps, targets, h_prev):
        """
        Performs Backpropagation Through Time (BPTT).
        Returns:
            - dWxh, dWhh, dWhy: Gradients for the weight matrices
            - dbh, dby: Gradients for the bias vectors
        """
        # Initialize gradients
        dWxh, dWhh, dWhy = np.zeros_like(self.Wxh), np.zeros_like(self.Whh), np.zeros_like(self.Why)
        dbh, dby = np.zeros_like(self.bh), np.zeros_like(self.by)
        
        # Initialize the gradient for the next hidden state
        dhnext = np.zeros_like(hs[0])

        # Backward pass through time
        for t in reversed(range(len(xs))):
            # The gradient of the loss with respect to the output scores (y)
            # For cross-entropy loss, this is simply (p - target)
            dy = np.copy(ps[t])
            dy[targets[t]] -= 1
            
            # Gradients for the output layer
            dWhy += np.dot(dy, hs[t].T)
            dby += dy
            
            # Backpropagate into the hidden state
            dh = np.dot(self.Why.T, dy) + dhnext
            # Backpropagate through the tanh non-linearity
            dhraw = (1 - hs[t] * hs[t]) * dh
            
            # Gradients for the biases and recurrent weights
            dbh += dhraw
            dWxh += np.dot(dhraw, xs[t].T)
            
            # --- FIX IS HERE ---
            # When t=0, there is no hs[t-1]. We must use the h_prev from the start of the sequence.
            if t > 0:
                dWhh += np.dot(dhraw, hs[t-1].T)
            else:
                dWhh += np.dot(dhraw, h_prev.T)
            
            # Save the gradient for the next time step
            dhnext = np.dot(self.Whh.T, dhraw)
            
        # To prevent exploding gradients, we clip them
        for dparam in [dWxh, dWhh, dWhy, dbh, dby]:
            np.clip(dparam, -5, 5, out=dparam)
            
        return dWxh, dWhh, dWhy, dbh, dby

    def update_params(self, dWxh, dWhh, dWhy, dbh, dby, lr):
        """Updates the model parameters using Stochastic Gradient Descent."""
        self.Wxh += -lr * dWxh
        self.Whh += -lr * dWhh
        self.Why += -lr * dWhy
        self.bh += -lr * dbh
        self.by += -lr * dby

# --- Loss Function ---
def loss_fn(ps, targets):
    """Calculates the cross-entropy loss."""
    loss = 0
    for t in range(len(targets)):
        # Add a small epsilon to the log to prevent log(0)
        loss += -np.log(ps[t][targets[t], 0] + 1e-9)
    return loss

# --- Generation Function ---
def sample(model, seed_ix, n):
    """
    Sample a sequence of n integers from the model.
    `seed_ix` is the seed letter for the first time step.
    """
    x = np.zeros((vocab_size, 1))
    x[seed_ix] = 1
    h = np.zeros((hidden_size, 1))
    ixes = []
    
    for t in range(n):
        h = np.tanh(np.dot(model.Wxh, x) + np.dot(model.Whh, h) + model.bh)
        y = np.dot(model.Why, h) + model.by
        p = np.exp(y) / np.sum(np.exp(y))
        
        # Sample from the probability distribution
        ix = np.random.choice(range(vocab_size), p=p.ravel())
        x = np.zeros((vocab_size, 1))
        x[ix] = 1
        ixes.append(ix)
        
    return ixes

# --- Training Loop ---

# Initialize the RNN
rnn = RNN(vocab_size, hidden_size, vocab_size)

# Initialize memory variables for Adagrad (a more advanced optimizer)
mWxh, mWhh, mWhy = np.zeros_like(rnn.Wxh), np.zeros_like(rnn.Whh), np.zeros_like(rnn.Why)
mbh, mby = np.zeros_like(rnn.bh), np.zeros_like(rnn.by) # memory variables for Adagrad
smooth_loss = -np.log(1.0/vocab_size)*seq_length # loss at iteration 0

n, p = 0, 0
h_prev = np.zeros((hidden_size, 1)) # Initialize h_prev outside the loop

while n <= 50000:
    # Prepare inputs (we're sweeping from left to right in steps seq_length long)
    if p + seq_length + 1 >= len(data) or n == 0:
        h_prev = np.zeros((hidden_size, 1)) # reset RNN memory
        p = 0 # go from start of data
    inputs = [char_to_ix[ch] for ch in data[p:p+seq_length]]
    targets = [char_to_ix[ch] for ch in data[p+1:p+seq_length+1]]

    # Forward pass
    xs, hs, ys, ps, h_prev = rnn.forward(inputs, h_prev)

    # Calculate loss
    loss = loss_fn(ps, targets)
    smooth_loss = smooth_loss * 0.999 + loss * 0.001
    if n % 1000 == 0:
        print(f"Iteration {n}, Loss: {smooth_loss:.4f}")
        # Sample from the model to see how it's doing
        sample_ix = sample(rnn, inputs[0], 200)
        txt = ''.join(ix_to_char[ix] for ix in sample_ix)
        print(f'----\n {txt} \n----')

    # Backward pass (BPTT)
    # --- FIX IS HERE ---
    # Pass the h_prev from *before* the forward pass to the backward function
    dWxh, dWhh, dWhy, dbh, dby = rnn.backward(xs, hs, ps, targets, h_prev)

    # Update parameters with a more sophisticated optimizer (Adagrad)
    for param, dparam, mem in zip([rnn.Wxh, rnn.Whh, rnn.Why, rnn.bh, rnn.by],
                                  [dWxh, dWhh, dWhy, dbh, dby],
                                  [mWxh, mWhh, mWhy, mbh, mby]):
        mem += dparam * dparam
        param += -learning_rate * dparam / np.sqrt(mem + 1e-8) # adagrad update

    p += seq_length # move data pointer
    n += 1 # iteration counter