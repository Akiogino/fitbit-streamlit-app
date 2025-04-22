import requests

url = "http://localhost:8000/data-visualization"

# マークダウンファイルからDI_PROMPTを読み込む
with open("demo/di_prompt.md", "r", encoding="utf-8") as file:
    DI_PROMPT = file.read()

payload = {"text": DI_PROMPT}

response = requests.post(url, json=payload)

if response.status_code == 200:
    result = response.json()["result"]
    print(result)
    print("----------------------------------------")
else:
    print(f"Request failed with status code {response.status_code}")