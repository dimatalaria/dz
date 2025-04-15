
import json
from fastapi import FastAPI

app = FastAPI()


class Task:
    def __init__(self, task_id: int, name: str):
        self.task_id = task_id
        self.name = name
        self.status: bool = False

    @staticmethod
    def read_file(file_name: str):
        with open(file_name, 'r', encoding='utf-8') as file:
            tasks = json.load(file)
        return tasks

    def create_task(self, file_name):
        task = {
            "ID задачи": self.task_id,
            "Название": self.name,
            "Статус": self.status
        }

        try:
            with open(file_name, 'r', encoding='utf-8') as file:
                tasks = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            tasks = []

        tasks.append(task)

        with open(file_name, 'w', encoding='utf-8') as file:
            json.dump(tasks, file, ensure_ascii=False, indent=4)

        return f"Задача успешно создана: {task}"

    def put_task(self, file_name):

@app.get("/tasks")
def get_tasks():
    result = Task.read_file("tasks_file.json")
    return result


@app.post("/tasks")
def create_task(id_task: int, name: str):
    result = Task(id_task, name)
    return result.create_task("tasks_file.json")


@app.put("/tasks/{task_id}")
def update_task(task_id: int, name: str, status: bool):

    with open("tasks_file.json", 'r', encoding="utf-8") as file:
        tasks = json.load(file)

    for task in tasks:
        if task["ID задачи"] == task_id:
            task["Название"] = name
            task["Статус"] = status
            with open("tasks_file.json", 'w', encoding='utf-8') as file:
                json.dump(tasks, file, ensure_ascii=False, indent=4)
            return f"Задача c ID: {task_id} изменена успешно"

    return f"Задача c ID: {task_id} не найдена"


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    with open("tasks_file.json", 'r', encoding="utf-8") as file:
        tasks: list = json.load(file)

    for task in tasks:
        if task["ID задачи"] == task_id:
            tasks.remove(task)
            with open("tasks_file.json", 'w', encoding='utf-8') as file:
                json.dump(tasks, file, ensure_ascii=False, indent=4)
            return f"Задача с {task_id} удалена успешно"

    return f"Задача c ID: {task_id} не найдена"

