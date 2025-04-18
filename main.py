import requests
from fastapi import FastAPI
import uvicorn

app = FastAPI()
TOKEN = "hTlh5vaMOXNpmBCKp_mqGq3mc7RqYnU67G0RV96D"
LLM_TOKEN = "Bearer r4mA9kDU7s_T4T3g6vmYEzFBrc9n59StNw3aSOW3"
KEY = "67ffeb79b72e9cfaf7265010"
URL = f"https://{KEY}.mockapi.io/api/v1/tasks/"
MODEL = "@cf/meta/llama-3-8b-instruct"
API_BASE_URL = "https://api.cloudflare.com/client/v4/accounts/d1cef1f4fd721e9aa8e5df5cb6b8bdfc/ai/run/"

class ApiLLM:
    def __init__(self, model: str, api_url: str):
        self.model = model
        self.api_url = api_url


    def get_result(self, task_name: str):

        headers = {"Authorization": LLM_TOKEN}

        inputs = [
            {"role": "system", "content": "You are a friendly assistan that helps write stories"},
            {"role": "user", "content": task_name}
        ]

        data = {"messages": inputs}

        response = requests.post(f"{self.api_url}{self.model}", headers=headers, json=data)

        return response.json()


class Task:

    def __init__(self, name: str, ii_helper: ApiLLM):
        self.name = name
        self.status: bool = False
        self.ii_helper = ii_helper

    @staticmethod
    def get_tasks(url):
        response = requests.get(url)
        return response.json()


    def create_task(self, url: str, ):

        data = {
            "name": self.name,
            "status": self.status
        }

        requests.post(url, json=data)

        response = self.ii_helper.get_result(self.name)

        return response


    @staticmethod
    def put_task(url: str, task_id: int, name: str, status: bool):

        data = {
            "id": task_id,
            "name": name,
            "status": status
        }

        response = requests.put(url + f'{task_id}', json=data)

        return response.json()


    @staticmethod
    def delete_task(url: str, task_id: int):
        response = requests.delete(url + f'{task_id}')
        return response.json()


ii = ApiLLM(MODEL, API_BASE_URL)

@app.get("/tasks")
def get_tasks():
    result = Task.get_tasks(url=URL)
    return result


@app.post("/tasks")
def create_task(name: str):
    result = Task(name, ii)
    return result.create_task(URL)


@app.put("/tasks/{task_id}")
def update_task(task_id: int, name: str, status: bool):
    return Task.put_task(url=URL,task_id=task_id,name=name, status=status)


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    return Task.delete_task(URL, task_id)


if __name__ == "__main__":
    uvicorn.run(
        'main:app')
