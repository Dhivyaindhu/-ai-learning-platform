# ai_engine/rag/vectorstore.py
# Unified vector store for assessment questions AND course content

import numpy as np
from typing import List, Dict, Any
import re
from collections import Counter
import math


class VectorStore:
    """
    Unified vector store using TF-IDF for similarity search.
    Works for both assessment questions and course content.
    No external dependencies (no FAISS, no sentence-transformers).
    """
    
    def __init__(self, collection_name="default"):
        self.collection_name = collection_name
        self.documents = []
        self.metadatas = []
        self.vectors = []
        self.vocabulary = {}
        self.idf = {}
        print(f"📦 VectorStore '{collection_name}' initialized")
    
    def add_documents(self, documents: List[str], metadatas: List[Dict[str, Any]]):
        """
        Add documents to the vector store.
        
        Args:
            documents: List of text strings to index
            metadatas: List of metadata dicts (same length as documents)
        """
        if len(documents) != len(metadatas):
            raise ValueError(f"documents ({len(documents)}) and metadatas ({len(metadatas)}) must have same length")
        
        self.documents = documents
        self.metadatas = metadatas
        
        # Build vocabulary from all documents
        all_words = set()
        for doc in documents:
            words = self._tokenize(doc)
            all_words.update(words)
        
        self.vocabulary = {word: idx for idx, word in enumerate(sorted(all_words))}
        
        # Calculate IDF (Inverse Document Frequency)
        self._calculate_idf(documents)
        
        # Vectorize all documents
        self.vectors = []
        for doc in documents:
            vec = self._vectorize(doc)
            self.vectors.append(vec)
        
        print(f"   ✅ Indexed {len(documents)} documents | Vocab: {len(self.vocabulary)} words")
    
    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text into words."""
        text = text.lower()
        # Remove punctuation and split
        words = re.findall(r'\b\w+\b', text)
        return words
    
    def _calculate_idf(self, documents: List[str]):
        """Calculate IDF scores for vocabulary."""
        num_docs = len(documents)
        word_doc_count = Counter()
        
        for doc in documents:
            unique_words = set(self._tokenize(doc))
            for word in unique_words:
                word_doc_count[word] += 1
        
        # IDF = log(total_docs / (1 + docs_containing_word))
        self.idf = {}
        for word in self.vocabulary:
            self.idf[word] = math.log(num_docs / (1 + word_doc_count.get(word, 0)))
    
    def _vectorize(self, text: str) -> np.ndarray:
        """Convert text to TF-IDF vector."""
        words = self._tokenize(text)
        word_counts = Counter(words)
        
        # Create TF-IDF vector
        vec = np.zeros(len(self.vocabulary))
        
        for word, count in word_counts.items():
            if word in self.vocabulary:
                idx = self.vocabulary[word]
                tf = count / len(words) if words else 0  # Term Frequency
                vec[idx] = tf * self.idf.get(word, 0)    # TF-IDF
        
        # L2 normalization
        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm
        
        return vec
    
    def similarity_search(self, query: str, k: int = 3, min_similarity: float = 0.0) -> List[Dict[str, Any]]:
        """
        Search for k most similar documents.
        
        Args:
            query: Search query string
            k: Number of results to return
            min_similarity: Minimum similarity threshold (0-1)
        
        Returns:
            List of dicts with keys: 'document', 'metadata', 'similarity'
        """
        if not self.vectors:
            print("   ⚠️ VectorStore is empty, no results")
            return []
        
        # Vectorize query
        query_vec = self._vectorize(query)
        
        # Calculate cosine similarities
        similarities = []
        for idx, doc_vec in enumerate(self.vectors):
            sim = np.dot(query_vec, doc_vec)  # Cosine similarity (vectors are normalized)
            if sim >= min_similarity:
                similarities.append((sim, idx))
        
        # Sort by similarity (descending)
        similarities.sort(reverse=True)
        
        # Return top k results
        results = []
        for sim, idx in similarities[:k]:
            results.append({
                'document': self.documents[idx],
                'metadata': self.metadatas[idx],
                'similarity': float(sim),
            })
        
        return results
    
    def get_all_documents(self) -> List[Dict[str, Any]]:
        """Return all documents with metadata."""
        return [
            {'document': doc, 'metadata': meta}
            for doc, meta in zip(self.documents, self.metadatas)
        ]
    
    def filter_by_metadata(self, key: str, value: Any) -> List[Dict[str, Any]]:
        """Filter documents by metadata field."""
        results = []
        for doc, meta in zip(self.documents, self.metadatas):
            if meta.get(key) == value:
                results.append({'document': doc, 'metadata': meta})
        return results
    
    def __len__(self):
        return len(self.documents)
    
    def __repr__(self):
        return f"VectorStore('{self.collection_name}', {len(self)} documents)"