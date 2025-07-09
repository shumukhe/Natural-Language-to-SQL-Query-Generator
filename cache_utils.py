from tinydb import TinyDB, Query
import os

# Initialize DB
db_path = "query_cache.json"
db = TinyDB(db_path)
Q = Query()

# Check if query already exists
def get_cached_result(nl_query):
    result = db.search(Q.query == nl_query)
    return result[0] if result else None

# Save query, SQL and result
def save_to_cache(nl_query, sql_query, result_data):
    # Check if this query already exists
    existing = db.search(Q.query == nl_query)
    
    if existing:
        db.update({
            "sql": sql_query,
            "result": result_data
        }, Q.query == nl_query)
    else:
        db.insert({
            "query": nl_query,
            "sql": sql_query,
            "result": result_data
        })

def clean_cache_duplicates():
    all_entries = db.all()
    seen = {}

    # This will keep the last inserted entry for each query
    for entry in all_entries:
        seen[entry["query"]] = entry

    # Clear DB and re-insert only unique entries
    db.truncate()
    for entry in seen.values():
        db.insert(entry)

    print(f"🧹 Removed duplicates. Now {len(seen)} unique entries remain.")


# Optional test
if __name__ == "__main__":
    clean_cache_duplicates()
