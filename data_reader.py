import sys

import chromadb
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore

load_dotenv()

CT_RAG_COLLECTION = "CT_RAG"


def read_index():
    embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

    print("Attempting to read from chromadb persistent store")
    db = chromadb.PersistentClient(path="./chroma_db")

    if CT_RAG_COLLECTION not in [col.name for col in db.list_collections()]:
        sys.exit(f"{CT_RAG_COLLECTION} was not found in Chroma. Exiting...")

    print("Reading the CT_RAG collection")
    ct_rag_collection = db.get_collection(CT_RAG_COLLECTION)

    if ct_rag_collection is None:
        print("CT_RAG collection was not found in Chroma DB")

    vector_store = ChromaVectorStore(chroma_collection=ct_rag_collection)

    print("Converting chroma collection to vector store index")
    index = VectorStoreIndex.from_vector_store(
        vector_store=vector_store,
        embed_model=embed_model
    )
    return index


if __name__ == "__main__":
    index = read_index()
    print(index.index_id)
