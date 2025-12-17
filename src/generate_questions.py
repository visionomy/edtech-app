import google.genai as genai
import json
import os

from dotenv import load_dotenv

from clients import _groq_client

load_dotenv()


client = _groq_client.GroqClient()
n_questions = 1

with open("../data/questions.json", "at") as fid:
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
            )
            print(json.dumps(result, indent=2))

            fid.write("\n")
            json.dump(result, fid)
