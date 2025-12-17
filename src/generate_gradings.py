import copy
import json

from dotenv import load_dotenv

from clients import _groq_client

load_dotenv()


with open("../data/questions.json", "rt") as fid:
    questions = json.load(fid)

qr_dict = {
    qi["question"]: qi["rubric"]
    for qi in questions
}

try:
    with open("../data/answers.json", "rt") as fid:
        answers = json.load(fid)
except json.JSONDecodeError:
    answers = []


def _grading_prompt(question, rubric, answer):
    return \
f"""You are an expert assessor of 5th Grade students. Given the question

{question}

and assessment rubric

{rubric}

give me an assessment of the student's answer:

{answer}

Instructions:
1. Evaluate each criterion carefully
2. Assign appropriate scores (can use decimals like 2.5)
3. Provide specific justification for each score
4. Give constructive feedback highlighting strengths and areas for improvement
5. Rate your confidence based on answer clarity and rubric applicability
"""


client = _groq_client.GroqClient()

gradings = []

with open("../data/gradings.json", "wt") as fid:
    for answer_dict in answers:
        grading_dict = copy.deepcopy(answer_dict)

        grading_dict["rubric"] = qr_dict[answer_dict["question"]]
        grading_dict["grading"] = client.request(
            _grading_prompt(answer_dict["question"], qr_dict[answer_dict["question"]], answer_dict["answer"]),
            temperature=1.5,
            output_schema="grading",
        )

        gradings.append(grading_dict)
    
    json.dump(gradings, fid, indent=4)
