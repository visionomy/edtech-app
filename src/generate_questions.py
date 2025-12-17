import json

from dotenv import load_dotenv

from clients import _groq_client

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
                f"""You are an expert assessor whose subject is {subject}. Give me an example exam question on the topic of {topic} suitable, complete with a corresponding rubric for assessment, for a 6th Grade student that can be answered in 100-200 words.""",
                temperature=1.5,
                output_schema="question",
            )
            print(json.dumps(result, indent=2))

            questions.append(result)
    
    json.dump(questions, fid, indent=4)
