from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from db_utils import extract_schema_from_sqlite

import os
import pickle

def create_vectorstore_from_schema(db_path, save_dir):
    # Step 1: Extract schema from SQLite
    schema_strings = extract_schema_from_sqlite(db_path)
    documents = [Document(page_content=s) for s in schema_strings]

    # Step 2: Create save directory if it doesn't exist
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        print(f"📁 Created directory: {save_dir}")

    # Step 3: Save documents for BM25 retrieval
    bm25_path = os.path.join(save_dir, "bm25_docs.pkl")
    with open(bm25_path, "wb") as f:
        pickle.dump(documents, f)
    print(f"✅ BM25 documents saved to {bm25_path}")

    # Step 4: Create and save FAISS vector store
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(documents, embedding_model)
    vectorstore.save_local(save_dir)
    print(f"✅ FAISS vectorstore saved to {save_dir}")
    print("📦 Files created:")
    print(f" - {os.path.join(save_dir, 'index.faiss')}")
    print(f" - {os.path.join(save_dir, 'index.pkl')}")
    print(f" - {bm25_path}")

# Run directly to test
if __name__ == "__main__":
    create_vectorstore_from_schema("data/Chinook.sqlite", "vectorstore_dir")
