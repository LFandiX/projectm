import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import numpy as np

def calculate_perplexity(text, model_name='gpt2'):
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    model = GPT2LMHeadModel.from_pretrained(model_name)
    model.eval()

    inputs = tokenizer(text, return_tensors='pt')
    input_ids = inputs['input_ids']

    with torch.no_grad():
        outputs = model(input_ids, labels=input_ids)
        loss = outputs.loss
        perplexity = torch.exp(loss)
    
    return perplexity.item()

# Contoh Penggunaan:
text_sample = "Pasar merupakan tempat bertemunya penjual dan pembeli untuk melakukan transaksi."
pps = calculate_perplexity(text_sample)
print(f"Perplexity Score: {pps:.2f}")
# Catatan: Teks AI biasanya punya skor < 20-30 (tergantung model)