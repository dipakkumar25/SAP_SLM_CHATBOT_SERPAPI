import faiss
import numpy as np
from typing import List, Tuple, Optional
from .embedding_model import EmbeddingModel

class SearchEngine:
    def __init__(self, embedding_model: EmbeddingModel):
        self.embedding_model = embedding_model
        self.index: Optional[faiss.IndexFlatL2] = None
        self.kb_texts: List[str] = []
    
    def build_index(self, texts: List[str]) -> None:
        """Build FAISS index from texts."""
        self.kb_texts = texts
        embeddings = self.embedding_model.encode(texts)
        
        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(np.array(embeddings))
    
    def search(self, query: str, k: int = 3, threshold: float = 0.7) -> List[Tuple[str, float]]:
        """Search for top-k similar texts."""
        if self.index is None:
            raise ValueError("Index not built. Call build_index() first.")
        
        query_vec = self.embedding_model.encode_single(query)
        D, I = self.index.search(np.array(query_vec), k)
        
        results = []
        for j, i in enumerate(I[0]):
            distance = D[0][j]
            if distance < threshold:
                results.append((self.kb_texts[i], distance))
        
        return results