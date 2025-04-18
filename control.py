import requests


API_BASE_URL = "https://api.cloudflare.com/client/v4/accounts/d1cef1f4fd721e9aa8e5df5cb6b8bdfc/ai/run/"
headers = {"Authorization": "Bearer r4mA9kDU7s_T4T3g6vmYEzFBrc9n59StNw3aSOW3"}


def run(model, inputs):
    input = { "messages": inputs }
    response = requests.post(f"{API_BASE_URL}{model}", headers=headers, json=input)
    return response.json()


inputs = [
    { "role": "system", "content": "You are a friendly assistan that helps write stories" },
    { "role": "user", "content": "Write a short story about a llama that goes on a journey to find an orange cloud "}
]
output = run("@cf/meta/llama-3-8b-instruct", inputs)
print(output)