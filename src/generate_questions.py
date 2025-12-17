import json

from dotenv import load_dotenv

from clients import _groq_client
from prompts import prompt_to_generate_question_on

load_dotenv()


client = _groq_client.GroqClient()
n_questions = 1

try:
    with open("../data/questions.json", "rt") as fid:
        questions = json.load(fid)
except json.JSONDecodeError:
    questions = []


with open("../data/questions.json", "wt") as fid:
    subjects = [
        ("biology", "plant biology"), 
        ("physics", "energy"),
        ("literature", "poetry"),
        ("history", "the romans"),
        ("geography", "the weather"),
    ]

    for subject, topic in subjects:
        for iq in range(n_questions):
            result = client.request(
                prompt_to_generate_question_on(subject, topic),
                temperature=1.5,
                output_schema="question",
            )
            print(json.dumps(result, indent=2))

            questions.append(result)
    
    json.dump(questions, fid, indent=4)
