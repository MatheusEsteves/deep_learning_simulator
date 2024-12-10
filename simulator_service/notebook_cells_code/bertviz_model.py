import torch
import torch.nn as nn
from transformers import BertTokenizer
from bertviz import head_view, model_view
import matplotlib.pyplot as plt

VOCAB_SIZE = 30522  # Usando o vocabulário do BERT

# Definindo o modelo Transformer simples
class SimpleTransformer(nn.Module):
    def __init__(self, vocab_size, embed_size, num_heads):
        super(SimpleTransformer, self).__init__()
        
        self.embedding = nn.Embedding(vocab_size, embed_size)  # Embedding de 3 dimensões
        self.attention = nn.MultiheadAttention(embed_size, num_heads)  # Camada de atenção multi-cabeça
        self.fc = nn.Linear(embed_size, vocab_size)  # Camada de saída para predição de palavras

        self.d_k = int(embed_size/num_heads)
        self.n_heads = num_heads
        self.embed_size = embed_size

        # matrizes WQ, WK e WV que criaram as matrizes de
        # vetores Q, K e V para nossas cabeças de atenção
        self.Wq = nn.Linear(embed_size, embed_size)
        self.Wk = nn.Linear(embed_size, embed_size)
        self.Wv = nn.Linear(embed_size, embed_size)
        
    def forward(self, x):
        # Aplica o embedding
        x = self.embedding(x)
        
        # Transpor para formato adequado para a camada de atenção
        x = x.transpose(0, 1)  # A camada MultiheadAttention espera [seq_len, batch_size, embed_size]

        batch_size, seq_len, d_model = x.shape

        # Gera as matrizes de vetores Q, K e V
        Q = self.Wq(x)  # [seq_len, batch_size, embed_size]
        K = self.Wk(x)  # [seq_len, batch_size, embed_size]
        V = self.Wv(x)  # [seq_len, batch_size, embed_size]

        # Passando Q, K, V pela camada de atenção
        output, attention_weights = self.attention(Q, K, V)  # Aqui as entradas são as mesmas, mas isso pode ser alterado
        attention_weights = torch.tensor([[attention_weights.tolist()]])
        attention_output = output

        # A camada de saída
        output = self.fc(attention_output)
        return output, attention_weights


def train(model, input_ids, target, optimizer, criterion, vocab_size):
    model.train()
    optimizer.zero_grad()
    output, attention_weights = model(input_ids)  # Passa os dados pelo modelo
    output = output.transpose(0, 1)  # Reverter a transposição
    output = output.view(-1, vocab_size)  # Redimensionar para a forma correta
    target = target.view(-1)  # Redimensionar para a forma correta
    loss = criterion(output, target)  # Calcular a perda
    loss.backward()  # Retropropagar
    optimizer.step()  # Atualizar os pesos
    return loss.item(), attention_weights

# Função para visualizar os pesos de atenção
def visualize_attention(attention_weights, tokens, view_mode):
    # Usar BertViz para exibir os pesos de atenção
    if view_mode == 'head_view':
        head_view(attention_weights, tokens)
    elif view_mode == 'model_view':
        model_view(attention_weights, tokens)

# Inicializando o modelo
model = SimpleTransformer(VOCAB_SIZE, EMBED_SIZE, NUM_HEADS)

# Inicializando o tokenizador
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# Tokenizando o texto
inputs = tokenizer(TEXT_SENTENCE_TRAIN, return_tensors='pt')
input_ids = inputs['input_ids']  # IDs dos tokens

# Exibindo os tokens
tokens = tokenizer.convert_ids_to_tokens(input_ids[0])
print(f"Tokens: {tokens}")

# Definindo a função de perda e o otimizador
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
criterion = nn.CrossEntropyLoss()

# Executando o treinamento (exemplo com apenas uma iteração)
loss, attention_weights = train(model, input_ids, input_ids, optimizer, criterion, VOCAB_SIZE)
print(f"Training loss: {loss}")

# Visualizando os pesos de atenção
visualize_attention(attention_weights, tokens, VIEW_MODE)