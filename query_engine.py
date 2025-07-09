from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from langchain_huggingface import HuggingFaceEmbeddings
from cache_utils import get_cached_result, save_to_cache
import sqlite3

from dotenv import load_dotenv
import os
import pickle

load_dotenv()

# Load FAISS vectorstore (semantic retriever)
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
faiss_vectorstore = FAISS.load_local("vectorstore_dir", embedding_model, allow_dangerous_deserialization=True)
semantic_retriever = faiss_vectorstore.as_retriever()
semantic_retriever.search_kwargs['k'] = 2

# Load BM25 retriever from saved pickle file
with open("vectorstore_dir/bm25_docs.pkl", "rb") as f:
    bm25_documents = pickle.load(f)
bm25_retriever = BM25Retriever.from_documents(bm25_documents)
bm25_retriever.k = 0  # You can adjust this

# Create hybrid retriever
hybrid_retriever = EnsembleRetriever(
    retrievers=[semantic_retriever, bm25_retriever],
    weights=[0.6, 0.4]
)

# Define LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",  # or "gpt-3.5-turbo"
    temperature=0.2,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# Define prompt template
template = """
You are an expert SQL assistant. Generate SQL queries based on the user question and the given schema.

Only use the tables and columns mentioned in this schema context:
{context}

User question: {question}

Respond with only the SQL query.
"""

prompt = ChatPromptTemplate.from_template(template)

# Chain = prompt | llm
chain: RunnableSequence = prompt | llm

import re

# Clean SQL before executing
def clean_sql(sql_text):
    # Remove ```sql and ```
    cleaned = re.sub(r"```sql|```", "", sql_text).strip()
    return cleaned

# Final SQL generation function
def generate_sql(user_question, db_path="Data/Chinook.sqlite"):
    sql_query = ""  # <--- PREVENTS undefined sql_query in exception block
    try:
        # ✅ Step 1: Check cache
        cached = get_cached_result(user_question)
        if cached and cached["result"]:
            print("⚡ Fetched from cache")
            return cached["sql"], cached["result"]

        # ❌ Step 2: Generate SQL from query
        retrieved_docs = hybrid_retriever.invoke(user_question)
        context = "\n".join(doc.page_content for doc in retrieved_docs)
        response = chain.invoke({"question": user_question, "context": context})
        sql_query = response.content.strip()
        sql_query = clean_sql(sql_query)

        # ✅ Step 3: Execute SQL on SQLite DB
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(sql_query)
        result_rows = cursor.fetchall()
        col_names = [description[0] for description in cursor.description]
        conn.close()

        # Package result as list of dicts (Streamlit friendly)
        result = [dict(zip(col_names, row)) for row in result_rows]

        # ✅ Step 4: Save to cache
        save_to_cache(user_question, sql_query, result)
        print(f"✅ Saved to cache: {user_question}")

        return sql_query, result

    except Exception as e:
        return f"❌ Error: {str(e)}\n\nSQL: {sql_query}", []



# Optional: quick test
if __name__ == "__main__":
    q = "Which employees have helped the most customers in Canada?"
    sql, result = generate_sql(q)
    print("Generated SQL:\n", sql)
    print("\nResults:\n", result)
