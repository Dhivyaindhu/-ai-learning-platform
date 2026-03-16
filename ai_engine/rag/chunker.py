# ai_engine/rag/chunker.py
# Text chunking utilities for RAG pipeline

import re


def chunk_text(doc, size=500, overlap=50):
    """
    Split text/document into chunks for better retrieval.

    Args:
        doc: Either a string or a document dictionary
        size: Chunk size in characters
        overlap: Overlap between chunks

    Returns:
        List of text chunks or document chunks
    """
    # Handle different input types
    if isinstance(doc, dict):
        # Extract text content from document
        text = doc.get('content', '')
        metadata = doc.get('metadata', {})

        # Chunk the text
        chunks = []
        i = 0
        while i < len(text):
            chunk_text = text[i:i + size]

            # Create chunk document
            chunks.append({
                'content': chunk_text,
                'metadata': metadata.copy()
            })

            i += size - overlap

        return chunks if chunks else [doc]

    elif isinstance(doc, str):
        # Simple string chunking
        text = doc
        chunks = []
        i = 0
        while i < len(text):
            chunks.append(text[i:i + size])
            i += size - overlap

        return chunks if chunks else [text]

    else:
        # Unknown type, return as-is in a list
        return [doc]


def chunk_documents(documents, chunk_size=500, overlap=50):
    """
    Chunk multiple documents.

    Args:
        documents: List of documents (strings or dicts)
        chunk_size: Size of each chunk
        overlap: Overlap between chunks

    Returns:
        List of all chunks from all documents
    """
    all_chunks = []

    for doc in documents:
        chunks = chunk_text(doc, size=chunk_size, overlap=overlap)
        all_chunks.extend(chunks)

    return all_chunks


def smart_chunk_text(text, chunk_size=500, overlap=50):
    """
    Smarter chunking that tries to break at sentence boundaries.

    Args:
        text: Text to chunk
        chunk_size: Target chunk size
        overlap: Overlap between chunks

    Returns:
        List of text chunks
    """
    if not text:
        return []

    # Split by sentences (simple approach)
    sentences = re.split(r'(?<=[.!?])\s+', text)

    chunks = []
    current_chunk = ""

    for sentence in sentences:
        # If adding this sentence exceeds chunk size
        if len(current_chunk) + len(sentence) > chunk_size and current_chunk:
            chunks.append(current_chunk.strip())
            # Start new chunk with overlap
            if overlap > 0:
                words = current_chunk.split()
                overlap_text = ' '.join(words[-overlap // 10:]) if words else ""
                current_chunk = overlap_text + " " + sentence
            else:
                current_chunk = sentence
        else:
            current_chunk += " " + sentence if current_chunk else sentence

    # Add the last chunk
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks