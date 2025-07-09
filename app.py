import streamlit as st
from query_engine import generate_sql

st.set_page_config(page_title="🧠 NL-to-SQL Assistant", layout="centered")

# Styling
st.markdown("""
    <style>
        .big-title {
            font-size: 2.5em;
            font-weight: bold;
            color: #4CAF50;
        }
        .subtle {
            color: #777;
        }
        .result-box {
            background-color: #f9f9f9;
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #ddd;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<div class='big-title'>🧠 Natural Language to SQL Assistant</div>", unsafe_allow_html=True)
st.markdown("<p class='subtle'>Ask a question about your database in natural language.</p>", unsafe_allow_html=True)

# User input
user_query = st.text_input("💬 Your Question:", placeholder="e.g. Show all customers from Canada")

# Run button
if st.button("Generate SQL") and user_query:
    with st.spinner("Thinking..."):
        sql_query, result = generate_sql(user_query)

    # Show generated SQL
    st.markdown("#### 🧠 Generated SQL Query")
    st.code(sql_query, language="sql")

    # Show execution result
    if result:
        st.markdown("#### 📊 Results")
        st.dataframe(result, use_container_width=True)
    else:
        st.warning("No results found or query failed to execute.")

# Footer
st.markdown("""
---
<p style='text-align: center; font-size: 0.85em;'>Built with ❤️ using LangChain, GPT-4o-mini, and Streamlit</p>
""", unsafe_allow_html=True)
