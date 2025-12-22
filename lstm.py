# No training, I am just trying to figure out the implementation

import torch
import torch.nn
import torch.nn.Functional as F

class simonLSTMCell(nn.Module):
    def __init__(self, input_size, hidden_size) -> None:
        super().__init__()
    
        self.input_size = input_size
        self.hidden_size = hidden_size

        self.W_ii = nn.Linear(input_size, hidden_size)
        self.W_if = nn.Linear(input_size, hidden_size) # Forget gate
        self.W_ig = nn.Linear(input_size, hidden_size) # Candidate gate
        self.W_io = nn.Linear(input_size, hidden_size)

        self.U_ii = nn.Linear(input_size, hidden_size)
        self.U_if = nn.Linear(input_size, hidden_size)
        self.U_ig = nn.Linear(input_size, hidden_size)
        self.U_io = nn.Linear(input_size, hidden_size)

    def forward(self, x, h_prev, c_prev):
        f_t = torch.sigmoid(self.W_if(x) + self.U_if(h_prev))
        i_t = torch.sigmoid(self.W_ii(x) + self.U_ii(h_prev))
        g_t = torch.sigmoid(self.W_ig(x) + self.U_ig(h_prev))
        o_t = torch.sigmoid(self.W_io(x) + self.W_io(h_prev))

        c_next = f_t * c_prev + i_t * g_t
        h_next = o_t * torch.tanh(c_next)

class simonLSTM(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers=1):
        super().__init__()

        self.num_layers = num_layers
        self.hidden_size = hidden_size

        self.lstm_cells = nn.ModuleList(\
                simonLSTMCell(input_size if i == 0 else hidden_size, hidden_size)\
                for i in range(num_layers))

    def forward(self, x):
        batch_size = x.size(0)
        seq_len = x.size(1)

        h = torch.zeros(batch_size, self.hidden_size).to(x.device)
        c = torch.zeros(batch_size, self.hidden_size).to(x.device)

        for t in range(seq_len):
            for layer in range(self.num_layers):
                h, c = self.lstm_cells[layer](x[:, t, :], h, c)
        return h, c


input_size = 10 # Input Features
hidden_size = 20
seq_len = 5
batch_size = 3

x = torch.randn(batch_size, seq_len, input_size)

model = simonLSTM(input_size=input_size, hidden_size=hidden_size)

h, c = model(x)
print("Hidden Shape: ", h.shape)
print("Cell shape: ", h.shape)
