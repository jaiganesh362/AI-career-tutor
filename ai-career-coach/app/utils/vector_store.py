# app/utils/vector_store.py

import faiss
import os
import pickle
import numpy as np

# Paths
VECTOR_PATH = "data/faiss_index/vectors.npy"
CHUNKS_PATH = "data/faiss_index/chunks.pkl"

# Save vectors + chunks
def save_vectorstore(vectors, chunks):
    if not os.path.exists("data/faiss_index"):
        os.makedirs("data/faiss_index")
    faiss_index = faiss.IndexFlatL2(len(vectors[0]))
    faiss_index.add(np.array(vectors).astype("float32"))
    faiss.write_index(faiss_index, "data/faiss_index/index.faiss")

    np.save(VECTOR_PATH, vectors)
    with open(CHUNKS_PATH, "wb") as f:
        pickle.dump(chunks, f)

# Load + search
def search_similar_chunks(query, top_k=5):
    if not (os.path.exists("data/faiss_index/index.faiss") and os.path.exists(CHUNKS_PATH)):
        return []

    # Load index
    faiss_index = faiss.read_index("data/faiss_index/index.faiss")
    with open(CHUNKS_PATH, "rb") as f:
        chunks = pickle.load(f)

    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer("all-MiniLM-L6-v2")
    query_vector = model.encode([query])
    D, I = faiss_index.search(np.array(query_vector).astype("float32"), top_k)
    return [chunks[i] for i in I[0]]
