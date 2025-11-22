import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class Retriever:
    def __init__(self, model_name="all-MiniLM-L6-v2", docs_folder="data/docs"):
        self.model = SentenceTransformer(model_name)
        self.docs_folder = docs_folder
        self.documents = []
        self.index = None

    def load_all_documents(self):
        self.documents = []
        files = []


        # Load all .txt files
        for filename in os.listdir(self.docs_folder):
            if filename.endswith(".txt"):
                files.append(os.path.join(self.docs_folder, filename))

        for file_path in files:
            with open(file_path, "r", encoding="utf-8") as f:
                full_text = f.read()

            chunks = full_text.split("\n\n")

            for chunk in chunks:
                cleaned = chunk.strip()
                if len(cleaned) > 5:
                    self.documents.append({
                        "text": cleaned,
                        "meta": os.path.basename(file_path)
                    })

        self._build_index()

    def _build_index(self):
        texts = [d["text"] for d in self.documents]
        if not texts:
            print("⚠ No documents found")
            return

        embeddings = self.model.encode(texts, convert_to_numpy=True)

        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(embeddings)

    def get_top_k(self, query, k=5):
        if not self.index:
            return []

        query_emb = self.model.encode([query], convert_to_numpy=True)
        distances, indices = self.index.search(query_emb, k)

        results = []
        for idx, dist in zip(indices[0], distances[0]):
            if idx < 0: 
                continue
            results.append({
                "text": self.documents[idx]["text"],
                "meta": self.documents[idx]["meta"],
                "score": float(dist)
            })

        return results
