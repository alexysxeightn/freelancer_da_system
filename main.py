import os
from config import DATASET_PATH, OPENAI_API_KEY
from database import load_dataset_into_sqlite
from llm_utils import (
    generate_sql_query,
    generate_human_answer,
    is_safe_sql,
    clean_sql_query,
)
from logger import log_entry
from schema import schema_description
from cli import (
    console,
    show_welcome,
    get_user_question,
    print_answer,
    print_sql_query,
    log_progress,
)
import pandas as pd
import warnings

warnings.filterwarnings("ignore")

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# Загрузка данных
conn, df = load_dataset_into_sqlite(DATASET_PATH)
sample_data = df.head()


def execute_sql_query(query):
    try:
        result_df = pd.read_sql_query(query, conn)
        return result_df
    except Exception as e:
        return f"Ошибка при выполнении SQL: {e}"


if __name__ == "__main__":
    show_welcome()
    while True:
        question = get_user_question()
        if question.lower() == "exit":
            console.print("[blue]👋 До свидания!")
            break

        log_progress()
        sql_query = generate_sql_query(question, schema_description, sample_data)
        cleaned_sql = clean_sql_query(sql_query)

        if not is_safe_sql(cleaned_sql):
            console.print("[red]⚠️ Небезопасный SQL-запрос. Попробуйте другой вопрос.")
            continue

        print_sql_query(cleaned_sql)
        result = execute_sql_query(cleaned_sql)
        human_answer = generate_human_answer(question, result)

        print_answer(human_answer)

        # Логируем всё
        log_entry(
            query=question,
            sql_query=cleaned_sql,
            sql_result=str(result),
            answer=human_answer,
        )
