import requests

url = 'http://localhost:8000/api/grade'

json_content = {
    "question_text": "Write a paragraph (100-200 words) describing the daily life of a typical Roman family during the 2nd century AD. Discuss their homes, food, family roles, and typical leisure activities.",
    "answer_text": "The Romans never did anything for us. Apart from roads. And sanitation."
}

r = requests.post(url, json=json_content)

print(r.json())
