# ai_engine/rag/retriever.py

"""
Simple retriever implementation.
"""

from .embeddings import embed


class Retriever:
    """Document retriever using vector similarity"""

    def __init__(self, vector_store, embedding_model=None):
        """
        Initialize retriever.

        Args:
            vector_store: VectorStore instance
            embedding_model: Embedding model (optional, will use simple embed)
        """
        self.vector_store = vector_store
        self.embedding_model = embedding_model

    def retrieve(self, query, top_k=5, filters=None):
        """
        Retrieve relevant documents for a query.

        Args:
            query: Query string
            top_k: Number of results to return
            filters: Optional filters (dict)

        Returns:
            List of relevant documents
        """
        # Generate query embedding
        query_embedding = self._embed_query(query)

        # Search vector store
        results = self.vector_store.search(query_embedding, top_k=top_k * 2)

        # Get documents
        documents = []
        for idx, score in results:
            doc = self.vector_store.get_document(idx)
            if doc:
                # Apply filters if provided
                if filters:
                    if self._matches_filters(doc, filters):
                        documents.append({
                            'content': doc.get('content', ''),
                            'metadata': doc.get('metadata', {}),
                            'score': score
                        })
                else:
                    documents.append({
                        'content': doc.get('content', ''),
                        'metadata': doc.get('metadata', {}),
                        'score': score
                    })

                if len(documents) >= top_k:
                    break

        return documents

    def _embed_query(self, query):
        """Generate embedding for query"""
        if self.embedding_model:
            return self.embedding_model(query)
        else:
            # Use simple embedding
            embeddings = embed([query])
            return embeddings[0] if embeddings else []

    def _matches_filters(self, document, filters):
        """Check if document matches filters"""
        metadata = document.get('metadata', {})

        for key, value in filters.items():
            if metadata.get(key) != value:
                return False

        return True


def retrieve(query, chunks, vector_store, top_k=5):
    """
    Simple retrieve function (backward compatible).

    Args:
        query: Query string
        chunks: List of text chunks
        vector_store: VectorStore instance
        top_k: Number of results

    Returns:
        List of relevant chunks
    """
    # Create retriever
    retriever = Retriever(vector_store)

    # Retrieve documents
    results = retriever.retrieve(query, top_k=top_k)

    # Return chunks
    relevant_chunks = []
    for result in results:
        relevant_chunks.append(result['content'])

    return relevant_chunks