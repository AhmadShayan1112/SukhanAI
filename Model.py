import torch
import torch.nn as nn
import torch.nn.init as init
vocab_size = 17217 # Ensure vocab size is correct
embedding_dim = 256
hidden_size = 512
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")
import json

# Load vocabulary from the JSON file
with open('vocabulary.json', 'r', encoding='utf-8') as f:
    vocab_dict = json.load(f)
word = "aarzoo"
word_index = vocab_dict.get(word, None)
reverse_vocab_dict = {v: k for k, v in vocab_dict.items()}
indices = [3, 4, 5, 6]  # Example word indices
decoded_words = [reverse_vocab_dict.get(idx, "<UNK>") for idx in indices]

class Seq2Seq(nn.Module):
    def __init__(self,vocab_size,embedding_dimension,hidden_size):
        super(Seq2Seq, self).__init__()
        ## Encoder
        self.Encoder_embedding = nn.Embedding(vocab_size,embedding_dimension)
        self.batch_norm = nn.BatchNorm1d(embedding_dimension) 
        self.Encoder=nn.LSTM(embedding_dimension,hidden_size,2,batch_first=True)
        ##Decoder
        self.Decoder_Embedding = nn.Embedding(vocab_size,embedding_dimension)
        self.Decoder=nn.LSTM(embedding_dimension,hidden_size,2,batch_first=True)
        self.output_layer=nn.Linear(hidden_size,vocab_size)
        self._initialize_weights()
        self.norm = nn.LayerNorm(hidden_size)
    def _initialize_weights(self):
        for name, param in self.named_parameters():
            if "weight_ih" in name:  # Input-to-hidden weights
                init.xavier_uniform_(param, gain=nn.init.calculate_gain("tanh"))
            elif "weight_hh" in name:  # Hidden-to-hidden (recurrent) weights
                init.orthogonal_(param)
            elif "bias" in name:
                nn.init.zeros_(param)
    def forward(self,input_seq,target_seq):## the Data<---input_Data, the Target Data<---
        #Encoder
        Embedding_input = self.Encoder_embedding(input_seq)## -->(batch_Size,seq_len,embedding_dim)
        Embedding_input = self.batch_norm(Embedding_input.permute(0, 2, 1)).permute(0, 2, 1)
        encoder_output,(hidden,cell) = self.Encoder(Embedding_input)
        #print(f"Encoder Hidden Mean: {hidden.mean().item()}, Std Dev: {hidden.std().item()}")
        #print(f"Encoder Cell Mean: {cell.mean().item()}, Std Dev: {cell.std().item()}")
        hidden = torch.stack([self.norm(h) for h in hidden], dim=0)
        cell = torch.stack([self.norm(c) for c in cell], dim=0)
        encoder_output = self.norm(encoder_output)
        #Decoder
        Embedding_target= self.Decoder_Embedding(target_seq)
        Decoder_outputs,_= self.Decoder(Embedding_target,(hidden,cell))
        # Output Layer
        output = self.output_layer(Decoder_outputs)
        #output = output.view(input_seq.size(0), target_seq.size(1), -1)
        return output
model = Seq2Seq(vocab_size, embedding_dim, hidden_size)
model.to(device)
model.load_state_dict(torch.load('seq2seq_model.pth'))
model.eval()  # Set the model to evaluation mode for inference
import torch

# Check if GPU is available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

def generate_sequence(input_seq, max_len=10):
    # Convert input_seq (words) to indices based on vocab_dict
    input_indices = [vocab_dict.get(word, vocab_dict.get('<UNK>')) for word in input_seq]
    input_tensor = torch.tensor(input_indices, device=device).unsqueeze(0)  # Move to GPU

    # Start the decoder with the <start> token
    target_seq = torch.tensor([vocab_dict['<start>']], device=device).unsqueeze(0)  # Move to GPU
    generated_sequence = []
    hidden, cell = None, None

    # Set model to evaluation mode
    model.to(device)  # Move model to GPU
    model.eval()

    with torch.no_grad():
        for _ in range(max_len):
            output = model(input_tensor, target_seq)  # Forward pass
            predicted_idx = output.argmax(dim=-1)[:, -1].item()  # Get the predicted word index
            predicted_word = reverse_vocab_dict.get(predicted_idx, '<UNK>')

            if predicted_word == '<end>':
                break  # Stop when <end> token is generated
            
            generated_sequence.append(predicted_word)

            # Update the target sequence with the predicted word
            target_seq = torch.cat([target_seq, torch.tensor([[predicted_idx]], device=device)], dim=1)

    return generated_sequence

# Example usage of generating a sentence
