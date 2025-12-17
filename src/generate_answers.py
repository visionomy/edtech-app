import json

from dotenv import load_dotenv

from clients import _groq_client

load_dotenv()


with open("../data/questions.json", "rt") as fid:
    questions = json.load(fid)


def _answer_prompt(age, topic, the_question):

    return \
f"""You are a {age} year old student. Answer the following question on {topic} in 100-200 words.
        
Question: {the_question}
"""

client = _groq_client.GroqClient(model_name="llama-3.1-8b-instant")

answers = []

for question in questions:
    for age in [7, 11, 16]:
        result = {
            "question": question["question"],
            "answer": client.request(
                _answer_prompt(age, question["topic"], question["question"]),
                temperature=1.5,
                output_schema="answer",
            ),
            "age": age,
        }

        answers.append(result)


with open("../data/answers.json", "wt") as fid:
    json.dump(answers, fid, indent=2)
