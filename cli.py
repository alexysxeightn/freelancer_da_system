from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.progress import track

console = Console()


def show_welcome():
    console.print(
        Panel.fit(
            "[bold blue]Добро пожаловать в систему анализа фрилансеров!",
            title="Freelancer Analyzer",
        )
    )


def get_user_question():
    return Prompt.ask("\n[green]Введите ваш вопрос (или 'exit')")


def print_answer(answer):
    console.print(f"\n[bold magenta]🔍 Ответ:\n{answer}")


def print_sql_query(query):
    console.print(f"[dim]🔗 Сгенерированный SQL-запрос:\n{query}")


def log_progress():
    for _ in track(range(10), description="[cyan]Обработка запроса..."):
        pass
