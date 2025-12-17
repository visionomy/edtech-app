def prompt_to_generate_question_on(subject, topic):
    return \
f"""You are an expert assessor whose subject is {subject}. Give me an example exam question on the topic of {topic} suitable, complete with a corresponding rubric for assessment, for a 6th Grade student that can be answered in 100-200 words.""",


def prompt_to_answer(question, topic, age):
    return \
f"""You are a {age} year old student. Answer the following question on {topic} in 100-200 words.
        
Question: {question}
"""


def prompt_to_grade(answer, question, rubric):
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
