import json
from sentence_transformers import SentenceTransformer


with open('mylist.json', 'r', encoding='utf-8') as file:
    data = json.load(file)


model_name = 'all-mpnet-base-v2'  # Or 'all-MiniLM-L6-v2'
model = SentenceTransformer(model_name)

combined_text = [f"{article['title']} {article['description']}" for article in data]
combined_embeddings = model.encode(combined_text)
print(f"Shape of combined embeddings: {combined_embeddings.shape}")


for i, article in enumerate(data):
    article['combined_embedding'] = combined_embeddings[i]

print(data)