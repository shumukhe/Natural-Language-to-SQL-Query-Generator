# 🧠 NL2SQL - Natural Language to SQL Converter

[🔗 Live Demo](https://your-deployed-url.com)&#x20;

---

## 📋 Project Summary

NL2SQL is a powerful and intelligent application that translates natural language queries into executable SQL statements using a hybrid retrieval-augmented generation (RAG) pipeline. It leverages a semantic + keyword-based retrieval system to extract schema context from a database and uses an LLM (OpenAI GPT-4o-mini) to generate SQL queries. The project also includes SQL execution and result visualization, making it a complete NL-to-Insight pipeline.

---

## 🔄 Project Flow & Technologies Used

```mermaid
graph TD
    A[Natural Language Query] --> B{Check Cache}
    B -- Hit --> C[Return Cached SQL + Result]
    B -- Miss --> D[Retrieve Schema Context]
    D --> E[Use Hybrid Retriever (FAISS + BM25)]
    E --> F[Generate SQL with OpenAI GPT-4o-mini]
    F --> G[Execute SQL on SQLite DB]
    G --> H[Return Result]
    H --> I[Store in TinyDB Cache]
```

### 🛠️ Key Technologies

- **LangChain v0.2+**: For LLM pipelines and hybrid retrieval
- **OpenAI GPT-4o-mini**: For natural language to SQL generation
- **HuggingFace Embeddings**: For semantic search
- **FAISS**: Vector-based semantic retrieval
- **BM25**: Keyword-based retrieval
- **TinyDB**: Local caching of user queries and results
- **SQLite**: Target database for SQL execution
- **Streamlit (optional)**: For interactive frontend (if used)

---

## 💡 Sample Questions to Try

- `Which employees have helped the most customers in Canada?`
- `List all customers from USA.`
- `Show invoices issued in the year 2010.`
- `How many albums were sold by each employee in Germany?`

---

## 💻 How to Run Locally

1. **Clone the Repository**

```bash
git clone https://github.com/your-username/nl2sql.git
cd nl2sql
```

2. **Create a Virtual Environment**

```bash
conda create -n nl2sqlenv python=3.10
conda activate nl2sqlenv
```

3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

4. **Set Environment Variable**

Create a `.env` file in the root directory with your OpenAI key:

```env
OPENAI_API_KEY=your_openai_api_key
```

Or set it manually:

```bash
export OPENAI_API_KEY=your_openai_api_key
```

5. **Run the Main Script**

```bash
python query_engine.py
```

6. **(Optional) Run Streamlit App**

```bash
streamlit run app.py
```

---

## 📦 Project Structure

```
├── app.py                    # (Optional) Streamlit frontend
├── query_engine.py           # Main logic for NL to SQL conversion
├── rag_utils.py              # Schema extraction + hybrid retriever
├── db_utils.py               # SQLite schema parsing
├── cache_utils.py            # TinyDB cache management
├── vectorstore_dir/          # FAISS index + BM25 docs
├── Data/
│   └── Chinook.sqlite        # Sample SQLite database
└── query_cache.json          # Cached NL → SQL + results
```

---

## 🧐 Future Improvements

- ✅ Hybrid Retriever (semantic + keyword)
- ✅ Caching of queries and results
- ❌ Multi-turn interaction (can be added later)
- ❌ User authentication / query history per user
- ❌ Support for multiple databases

---

## 📬 Contact

For questions or suggestions, feel free to reach out via [LinkedIn](https://linkedin.com/in/your-profile) or raise an issue in the repo.

---

> 💡 This project is a great portfolio piece to showcase LLMOps, retrieval-augmented generation, and data engineering capabilities.

