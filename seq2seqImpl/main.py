import torch
import torch.nn as nn
import torch.optim as optim
from torchtext.datasets import Multi30k
from torchtext.data import Field, BucketIterator
import numpy as np
import spacy
import random
from torch.utils.tensorboard import SummaryWriter
from utils import translate_sentence, save_checkpoint, load_checkpoint

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

spacy_ger = spacy.load('de')
spacy_eng = spacy.load('en')

def tokenizer_ger(text):
        return [tok.text for tok in spacy_ger.tokenizer(text)]

def tokenizer_en(text):
        return [tok.text for tok in spacy_eng.tokenizer(text)]

german = Field(tokenize=tokenizer_ger, lower=True, init_token='<sos>',
               eos_token='<eos>')
english = Field(tokenize=tokenizer_en, lower=True, init_token='<sos>', eos_token='<eos>')

train_data, validation_data, test_data = Multi30k.splits(exts=('.de', '.en'),
                                                          fields=(german, english))
german.build_vocab(train_data, max_size = 10000, min_freq=2)
english.build_vocab(train_data, max_size=10000, min_freq=2)


class Encoder(nn.Module):
        def __init__(self, input_size, embedding_size, hidden_size, num_layers, p):  # p is for dropout
                super(Encoder, self).__init__()
                self.hidden_size = hidden_size
                self.num_layers = num_layers

                self.dropout = nn.Dropout(p)
                self.embedding = nn.Embedding(input_size, embedding_size)
                self.rnn = nn.LSTM(embedding_size, hidden_size=hidden_size, num_layers=num_layers, dropout=p)

        def forward(self, x):
                # x -> shape = (seq_length, N), where N is batch size
                embedding = self.dropout(self.embedding(x))
                # embedding -> shape = (seq_length, N, embedding_size)
                output, (hidden, cell) = self.rnn(embedding)
                return hidden, cell

class Decoder(nn.Module):
        def __init__(self, input_size, embedding_size, hidden_size, output_size,
                        num_layers, p):
                super(Decoder, self).__init__()
                self.hidden_size = hidden_size
                self.num_layers = num_layers
                self.dropout = nn.Dropout(p=p)
                self.embedding = nn.Embedding(input_size, embedding_size)
                self.rnn - nn.LSTM(embedding_size, hidden_size=hidden_size, num_layers=num_layers, dropout=p)

                self.fc = nn.Linear(hidden_size, output_size)
        def forward(self, x, hidden, cell): # from encoder(ctx vec)
                # x(shape) -> (N) but we do -> (1, N)
                x.unsqueeze(0)

                embedding = self.dropout(self.embedding(x))
                # embedding -> shape = (1, N, embedding_size)
                output, (hidden, cell) = self.rnn(embedding, (hidden, cell))
                # output -> shape = (1, N, hidden_size)
                predictions = self.fc(output)
                # predictions -> shape = (1, N, length_of_words)
                predictions = predictions.squeeze(0)
                # predictions -> shape = (N, length_of_words)
                return predictions, hidden, cell

class Seq2Seq(nn.Module):
        def __init__(self, encoder, decoder):
                super(Seq2Seq, self).__init__()
                self.encoder = encoder
                self.decoder = decoder

        def forward(self, source, target, teacher_force_ratio=0.5):
                batch_size = source.shape[1]
                # batch_size -> shape = (target_length, N), N is batch_size
                target_len = target.shape[0]
                target_vocab_size = len(english.vocab)

                outputs = torch.zeros(target_len, batch_size, target_vocab_size).to(device=device)

                hidden, cell = self.encoder(source)
                
                #get the starting token
                x = target[0]

                for t in range(1, target_len):
                        output, hidden, cell = self.decoder(x, hidden, cell)
                        outputs[t] = output
                        # (N, english_vocab_size)
                        best_guess = output.argmax(1)

                        x =  target[t] if random.random() < teacher_force_ratio else best_guess
                
                return outputs
                        

num_epochs = 20
learning_rate = 0.001
batch_size = 64

load_model = False
input_size_encoder = len(german.vocab)
input_size_decoder = len(english.vocab)
output_size = len(english.vocab)
encoder_embedding_size = 300
decoder_embedding_size = 300
hidden_size = 1024
num_layers = 4
encoder_dropout = 0.5
dec_dropout = 0.5

writer = SummaryWriter(f"runs/loss")
step = 0

train_iterator, validation_iterator, test_iterator = BucketIterator.splits(
        (train_data, validation_data, test_data),
        batch_size=batch_size, device=device)

encoder_net = Encoder(input_size=input_size_encoder, embedding_size=encoder_embedding_size,
                num_layers=num_layers, p=encoder_dropout).to(device=device)
decoder_net = Encoder(input_size=input_size_decoder, embedding_size=decoder_embedding_size, 
                hidden_size=hidden_size, num_layers=num_layers, p=dec_dropout).to(device=device)

model = Seq2Seq(encoder_net, decoder_net).to(device=device)

optimizer = optim.Adam(model.parameters(), lr=learning_rate)

pad_idx = english.vocab.stoi['<pad>']
criterion = nn.CrossEntropyLoss(ignore_index=pad_idx)

if load_model:
        load_checkpoint(torch.load('checkpoint.pth.ptar'), model, optimizer)

for epoch in range(num_epochs):
        print(f"Epoch {epoch}/{num_epochs}")

        checkpoint = {'state_dict':model.state_dict(), 'optimizer':optimizer.state_dict()}

        for batch_idx, batch in enumerate(train_iterator):
                inp_data = batch.src.to(device)
                target =  batch.trg.to(device)

                output = model(inp_data, target)
                #output -> shape = (trg_length, batch_size, output_dim)
                output = output[1:].reshape(-1, output.shape[2])
                target = target[1:].reshape(-1)

                optimizer.zero_grad()
                loss = criterion(output, target)
                loss.backward()

                torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1)
                optimizer.step()

                writer.add_scalar('Training Loss', loss, global_step=step) 
