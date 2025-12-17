import json
import os

from dotenv import load_dotenv
from groq import Groq

from .client import ClientBase

load_dotenv()


criterion_schema = {
    "type": "object",
    "properties": {
        "criterion": {
            "type": "string",
        },
        "max_score": {
            "type": "integer",
        },
        "justification": {
            "type": "string",
        },
    },
}

question_schema = {
    "description": "Schema that describes an exam question on a given subject and its assessment rubric",
    "name": "question-schema",
    "schema": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "properties": {
            "subject": {
                "type": "string",
            },
            "topic": {
                "type": "string",
            },
            "question": {
                "type": "string",
            },
            "rubric": {
                "type": "array",
                "items": criterion_schema,
            },
        },
    },
}

schemas = {
    "question": {"type": "json_schema", "json_schema": question_schema},
}

class GroqClient(ClientBase):

    def __init__(self, model_name="openai/gpt-oss-20b"):
        super().__init__(model_name)
        
        self._client = Groq(
            api_key=os.environ.get("GROQ_API_KEY"),
        )

    def request(self, content, temperature=None, output_schema=None):
        chat_completion = self._client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": content,
                }
            ],

            # See https://console.groq.com/docs/rate-limits 
            # See https://console.groq.com/docs/structured-outputs#supported-models

            # model="llama-3.3-70b-versatile",
            # model="llama-3.1-8b-instant",
            model=self._model_name, response_format=schemas.get(output_schema),

            temperature=temperature,
        )

        result = chat_completion.choices[0].message.content

        if schemas.get(output_schema) is not None:
            result = json.loads(result)
        
        return result
    