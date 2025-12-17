import json

from dotenv import load_dotenv

from clients import _groq_client
from prompts import prompt_to_answer

load_dotenv()


with open("../data/questions.json", "rt") as fid:
    questions = json.load(fid)

client = _groq_client.GroqClient(model_name="llama-3.1-8b-instant")

answers = []

for question in questions:
    for age in [7, 11, 16]:
        result = {
            "question": question["question"],
            "answer": client.request(
                prompt_to_answer(question["question"], question["topic"], age),
                temperature=1.5,
                output_schema="answer",
            ),
            "age": age,
        }

        answers.append(result)


with open("../data/answers.json", "wt") as fid:
    json.dump(answers, fid, indent=2)
