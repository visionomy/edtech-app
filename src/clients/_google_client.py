import google.genai as genai
import os

from dotenv import load_dotenv
from typing_extensions import TypedDict

from .client import ClientBase

load_dotenv()


class CriterionScore(TypedDict):
    criterion: str
    max_score: float
    justification: str


class QuestionAndRubric(TypedDict):
    subject: str
    question: str
    criterion_scores: list[CriterionScore]


class GoogleClient(ClientBase):

    def __init__(self, 
                 model_name='gemini-2.5-flash-lite',  # 20 RPD
                #  model_name="gemini-2.5-flash",
                #  model_name="gemma-3-4b-it",  # 14.4k RPD; no JSON :(
                #  model_name="gemini-2.5-flash",
        ):
        super().__init__(model_name)
        
        self._client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))

    def __del__(self):
        self._client.close()

    def request(self, content, temperature=None, output_schema=None):
        response = self._client.models.generate_content(
            model=self._model_name,

            config={
                "response_mime_type": "application/json",
                "response_schema": QuestionAndRubric,
                'temperature': 0.3,
                'top_p': 0.95,
                'top_k': 20,
            },
            contents={'text': content},
        )

        return response


# List of models that are available in v1beta:

# models/gemini-2.5-flash
# models/gemini-2.5-pro
# models/gemini-2.0-flash-exp
# models/gemini-2.0-flash
# models/gemini-2.0-flash-001
# models/gemini-2.0-flash-lite-001
# models/gemini-2.0-flash-lite
# models/gemini-2.0-flash-lite-preview-02-05
# models/gemini-2.0-flash-lite-preview
# models/gemini-exp-1206
# models/gemini-2.5-flash-preview-tts
# models/gemini-2.5-pro-preview-tts
# models/gemma-3-1b-it
# models/gemma-3-4b-it
# models/gemma-3-12b-it
# models/gemma-3-27b-it
# models/gemma-3n-e4b-it
# models/gemma-3n-e2b-it
# models/gemini-flash-latest
# models/gemini-flash-lite-latest
# models/gemini-pro-latest
# models/gemini-2.5-flash-lite
# models/gemini-2.5-flash-image-preview
# models/gemini-2.5-flash-image
# models/gemini-2.5-flash-preview-09-2025
# models/gemini-2.5-flash-lite-preview-09-2025
# models/gemini-3-pro-preview
# models/gemini-3-pro-image-preview
# models/nano-banana-pro-preview
# models/gemini-robotics-er-1.5-preview
# models/gemini-2.5-computer-use-preview-10-2025
# models/deep-research-pro-preview-12-2025

# via:

#     print("List of models that support generateContent:\n")
#     for m in client.models.list():
#         for action in m.supported_actions:
#             if action == "generateContent":
#                 print(m.name)

# Note that most of these don't support JSON output: https://ai.google.dev/gemini-api/docs/structured-output?example=recipe#model_support