import os
from typing import Optional
from dotenv import load_dotenv
from langchain_core.embeddings import Embeddings
from langchain_ollama import OllamaEmbeddings

load_dotenv()

def embedding(provider: Optional[str] = None, model: Optional[str] = None, base_url: Optional[str] = None):
    """
    Returns a normalized embedding function based on provider and model.
    
    Args:
        provider: Optional embedding provider name (defaults to env var EMBEDDING_PROVIDER or "ollama")
        model: Optional model name to use (overrides env var OLLAMA_EMBED_MODEL)
        base_url: Optional base URL for API (overrides env var VITE_OLLAMA_BASE_URL)
    
    Returns:
        Embeddings: A LangChain embeddings object
    """
    selected_provider = provider or os.getenv("EMBEDDING_PROVIDER", "ollama").lower()
    print(f"Selected embedding provider: {selected_provider}")

    base_embeddings: Embeddings

    if selected_provider == "ollama":
        ollama_base_url = base_url or os.getenv("VITE_OLLAMA_BASE_URL")
        ollama_model = model or os.getenv("OLLAMA_EMBED_MODEL")
        print(f"Using Ollama model: {ollama_model} at {ollama_base_url}")
        
        base_embeddings = OllamaEmbeddings(
            base_url=ollama_base_url,
            model=ollama_model,
        )
    else:
        raise ValueError(f"Unsupported embedding provider: '{selected_provider}'.")

    return base_embeddings