import json
from config import LOG_FILE


def log_entry(query, sql_query, sql_result, answer):
    entry = {
        "query": query,
        "llm_sql_query": sql_query,
        "result_sql_query": str(sql_result),
        "answer": answer,
    }
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
