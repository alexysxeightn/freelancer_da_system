from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from config import OPENAI_API_KEY, MODEL

llm = ChatOpenAI(model=MODEL, temperature=0, openai_api_key=OPENAI_API_KEY)


def generate_sql_query(question, schema_description, sample_data):
    prompt = f"""
        Ты — опытный аналитик данных и SQL-разработчик.
        Пользователь задал вопрос: "{question}"

        Вот описание таблицы `freelancers`:
        {schema_description}

        Пример первых строк таблицы:
        {sample_data.to_string(index=False)}

        Сгенерируй один SQL-запрос, который решает задачу.
        Запрос должен быть корректным, читаемым, безопасным, без команд удаления/модификации.
        Если это возможно, добейся запросом получения одного числа - ответа на вопрос (при этом будь внимателен, не всегда ответ только одно число).
        Не добавляй никаких комментариев и объяснений — только SQL-запрос.
        SQL:
    """
    response = llm([HumanMessage(content=prompt)])
    return response.content.strip()


def generate_human_answer(question, result):
    prompt = f"""
        На основе следующего вопроса и результата SQL-запроса, сформируй естественный, понятный ответ на русском языке. Ответ должен быть точен, без приближений и лишних деталей.

        Вопрос: "{question}"
        Результат: {result}

        Примеры:
        - Вопрос: "Какой средний доход фрилансеров?"
        Результат: 45000
        Ответ: Средний доход фрилансеров составляет 45 000 долларов США.

        - Вопрос: "Насколько выше доход у фрилансеров с криптой?"
        Результат: 1200
        Ответ: Доход фрилансеров, принимающих оплату в криптовалюте, на 1200 долларов США выше, чем у остальных.

        Сформируй такой же понятный ответ:
"""

    response = llm([HumanMessage(content=prompt)])
    return response.content.strip()


def is_safe_sql(query):
    dangerous_keywords = ["drop", "delete", "update", "insert", "alter", "--"]
    for word in dangerous_keywords:
        if word.lower() in query.lower():
            return False
    return True


def clean_sql_query(query):
    return query.replace("```sql", "").replace("```", "").strip()
