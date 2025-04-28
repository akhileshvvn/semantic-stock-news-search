import json
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss


with open('mylist.json', 'r', encoding='utf-8') as file:
    data = json.load(file)


model_name = 'all-mpnet-base-v2'  # Or 'all-MiniLM-L6-v2'
model = SentenceTransformer(model_name)

combined_text = [f"{article['title']} {article['description']}" for article in data]
combined_embeddings = model.encode(combined_text)
print(f"Shape of combined embeddings: {combined_embeddings.shape}")


for i, article in enumerate(data):
    article['combined_embedding'] = combined_embeddings[i]

# Assuming 'description_embeddings' is a NumPy array
embeddings = np.array(combined_embeddings).astype('float32')
embedding_dimension = embeddings.shape[1]
num_articles = embeddings.shape[0]

print(f"Shape of embedding matrix: {embeddings.shape}")
print(f"Embedding dimension: {embedding_dimension}")
print(f"Number of articles: {num_articles}")

index = faiss.IndexFlatIP(embedding_dimension)
index.add(embeddings)

def search_articles(query, model, index, articles, top_k=5):
    """
    Searches for the top_k most similar articles to a given query.

    Args:
        query (str): The user's search query.
        model (SentenceTransformer): The Sentence-BERT model used for embeddings.
        index (faiss.Index): The FAISS index containing the article embeddings.
        articles (list): The list of original news article dictionaries.
        top_k (int): The number of top results to return.

    Returns:
        list: A list of the top_k most similar articles (dictionaries).
    """
    query_embedding = model.encode([query]).astype('float32')
    distances, indices = index.search(query_embedding, top_k)

    results = []
    for i in range(len(indices[0])):
        article_index = indices[0][i]
        distance = distances[0][i]
        results.append({
            'article': articles[article_index],
            'similarity_score': distance  # Higher for IP, lower for L2
        })
    return results

query = "latest news on Tesla stock"
search_results = search_articles(query, model, index, data)

print(f"Top {len(search_results)} results for query: '{query}'\n")
for result in search_results:
    print(f"Title: {result['article']['title']}")
    print(f"Description: {result['article']['description']}")
    print(f"Similarity Score: {result['similarity_score']:.4f}")
    print("-" * 30)