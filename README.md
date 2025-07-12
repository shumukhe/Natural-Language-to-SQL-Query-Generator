🧠 Natural Language to SQL Query Generator
🔗 Live Demo <!-- Replace with actual deployed URL -->

🚀 Project Summary
This project allows users to ask natural language questions about a relational database and receive accurate SQL queries as output—automatically generated using Large Language Models (LLMs). It also executes the generated SQL on a local SQLite database and returns the results in tabular form. The system uses a hybrid retrieval mechanism (semantic + keyword search) to provide schema context and supports result caching to optimize performance and cost.

⚙️ Project Flow & Tech Stack
mermaid
Copy
Edit
flowchart TD
    A[User Inputs NL Query] --> B[Hybrid Retriever (FAISS + BM25)]
    B --> C[Relevant Schema Chunks]
    C --> D[Prompt with Context]
    D --> E[LLM (OpenAI GPT-4o-mini)]
    E --> F[SQL Query]
    F --> G[SQLite DB Execution]
    G --> H[Results in Table]
    F --> I[Cache Storage]
    H --> I
🔧 Technologies Used
Python 3.11+

LangChain (v0.2+)

OpenAI GPT-4o-mini (for SQL generation)

FAISS (for semantic vector search)

BM25Retriever (for keyword-based search)

TinyDB (for caching)

Streamlit (for UI, if deployed)

SQLite (Chinook database)

💬 Sample Questions to Try
These work well with the Chinook Database:

Which employees have helped the most customers in Canada?

List all customers from Brazil.

Show the top 5 customers by total purchase amount.

Find the genre that generated the most revenue.

🧪 How to Run Locally
🔨 Setup Instructions
Clone the Repository

bash
Copy
Edit
git clone https://github.com/your-username/nl-to-sql.git
cd nl-to-sql
Create & Activate Virtual Environment

bash
Copy
Edit
conda create -n nl2sqlenv python=3.11 -y
conda activate nl2sqlenv
Install Dependencies

bash
Copy
Edit
pip install -r requirements.txt
Add Your Environment Variables

Create a .env file in the root directory:

ini
Copy
Edit
OPENAI_API_KEY=your-openai-key
Prepare the Database and Vectorstore

Run the scripts in this order:

bash
Copy
Edit
python db_utils.py       # Extracts schema from Chinook DB
python rag_utils.py      # Creates hybrid retriever (FAISS + BM25)
Run the App or Query Engine

For Backend Testing:

bash
Copy
Edit
python query_engine.py
Or if you have a Streamlit UI:

bash
Copy
Edit
streamlit run app.py
📂 Folder Structure (Simplified)
bash
Copy
Edit
NL_to_SQL/
│
├── data/                  # Chinook SQLite DB
├── vectorstore_dir/      # Vector DB + BM25 docs
├── cache_utils.py        # Caching logic
├── db_utils.py           # Schema extraction
├── rag_utils.py          # Retriever creation
├── query_engine.py       # Core logic for SQL generation and execution
├── app.py                # Streamlit frontend (optional)
├── query_cache.json      # Stores past results
└── .env
