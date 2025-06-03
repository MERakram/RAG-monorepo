import os
from dotenv import load_dotenv
from apps.rag.embedding import embedding

__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from langchain_chroma import Chroma

# Load environment variables from the .env file in the rag directory
# Ensure the backend environment also loads these or they are set globally.
# The path to .env might need adjustment depending on how the backend runs.
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=dotenv_path)

COLLECTION_NAME = os.getenv("COLLECTION_NAME")
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Ensure the persist directory exists if needed for initialization (though Chroma handles it)
# os.makedirs(PERSIST_DIRECTORY, exist_ok=True)

_vector_store = None

def get_vector_store():
    """
    Initializes and returns a Chroma vector store instance.
    Caches the instance to avoid reloading on every call.

    Returns:
        Chroma: An instance of the Chroma vector store.
    """
    global _vector_store
    if _vector_store is None:
        if not COLLECTION_NAME:
            raise ValueError("COLLECTION_NAME environment variable not set.")
        if not './'+ COLLECTION_NAME:
             raise ValueError("Could not determine PERSIST_DIRECTORY for Chroma.")

        print(f"Initializing Chroma DB for collection: {COLLECTION_NAME}")
        print(f"Persistence directory: ./{COLLECTION_NAME}")

        embedding_function = embedding()

        _vector_store = Chroma(
            collection_name=COLLECTION_NAME,
            persist_directory='./'+COLLECTION_NAME,
            embedding_function=embedding_function,
        )
        print("Chroma DB initialized successfully.")
    return _vector_store

# Example of how to potentially preload or check connection on startup
# if __name__ == "__main__":
#     try:
#         db = get_vector_store()
#         print(f"Successfully connected to Chroma collection: {db._collection.name}")
#         # Optionally perform a dummy query or count
#         # print(f"Number of items in collection: {db._collection.count()}")
#     except Exception as e:
#         print(f"Error initializing Chroma DB: {e}")
