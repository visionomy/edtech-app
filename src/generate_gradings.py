import copy
import json

from dotenv import load_dotenv

from clients import _groq_client
from prompts import prompt_to_grade

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


client = _groq_client.GroqClient()

gradings = []

with open("../data/gradings.json", "wt") as fid:
    for answer_dict in answers:
        grading_dict = copy.deepcopy(answer_dict)
        
        grading_dict["grading"] = client.request(
            prompt_to_grade(
                answer_dict["answer"],
                answer_dict["question"],
                qr_dict[answer_dict["question"]]
            ),
            temperature=1.5,
            output_schema="grading",
        )

        gradings.append(grading_dict)
    
    json.dump(gradings, fid, indent=4)
