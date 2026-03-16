# ai_engine/rag/embeddings.py
# Simple embedding model wrapper for RAG

import numpy as np


class SimpleEmbeddingModel:
    """
    Simple embedding model using sentence transformers
    Falls back to TF-IDF if sentence transformers not available
    """
    
    def __init__(self):
        self.model = None
        self.use_transformer = False
        self.vectorizer = None
        
        # Try sentence transformers first (best quality)
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            self.use_transformer = True
            print("✅ Loaded sentence-transformers model")
        except ImportError:
            print("⚠️ sentence-transformers not available, using TF-IDF")
            from sklearn.feature_extraction.text import TfidfVectorizer
            self.vectorizer = TfidfVectorizer(max_features=384)
            self.corpus = []
    
    def embed_text(self, text):
        """
        Create embedding for text
        
        Returns:
            numpy array of shape (384,)
        """
        if self.use_transformer:
            # Use sentence transformer
            embedding = self.model.encode(text, convert_to_numpy=True)
            return embedding
        else:
            # Use TF-IDF (requires fitting on corpus)
            if not self.corpus:
                # First text, initialize
                self.corpus = [text]
                self.vectorizer.fit(self.corpus)
            
            # Add to corpus if new
            if text not in self.corpus:
                self.corpus.append(text)
                self.vectorizer.fit(self.corpus)
            
            # Get vector
            vec = self.vectorizer.transform([text]).toarray()[0]
            
            # Pad/truncate to 384 dimensions
            if len(vec) < 384:
                vec = np.pad(vec, (0, 384 - len(vec)))
            else:
                vec = vec[:384]
            
            return vec
    
    def embed_batch(self, texts):
        """
        Embed multiple texts
        
        Returns:
            numpy array of shape (n, 384)
        """
        if self.use_transformer:
            embeddings = self.model.encode(texts, convert_to_numpy=True)
            return embeddings
        else:
            return np.array([self.embed_text(t) for t in texts])


# Global instance
_embedding_model = None


def get_embedding_model():
    """Get or create global embedding model"""
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = SimpleEmbeddingModel()
    return _embedding_model


# Backward compatible function
def embed(texts):
    """
    Embed texts using global model
    
    Args:
        texts: List of text strings or list of dicts with 'content' key
    
    Returns:
        List of embedding vectors
    """
    model = get_embedding_model()
    
    # Extract text from dicts if needed
    text_list = []
    for t in texts:
        if isinstance(t, dict):
            text_list.append(t.get('content', ''))
        else:
            text_list.append(str(t))
    
    return model.embed_batch(text_list)