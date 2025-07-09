import sqlite3

def extract_schema_from_sqlite(db_path="data/Chinook.sqlite"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]

    schema_docs = []

    for table in tables:
        cursor.execute(f"PRAGMA table_info({table});")
        columns = cursor.fetchall()

        column_descriptions = []
        for col in columns:
            col_name = col[1]
            col_type = col[2]
            column_descriptions.append(f"- {col_name} ({col_type})")

        schema_text = f"""Table: {table}
Columns:
{chr(10).join(column_descriptions)}"""

        schema_docs.append(schema_text)

    conn.close()
    return schema_docs
