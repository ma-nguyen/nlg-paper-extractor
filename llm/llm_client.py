from openai import OpenAI
from llm.postprocessing import remove_think_blocks, remove_JSON_backticks
import json
from prompts.prompt import Prompt
from config import API_KEY, BASE_URL



class LLMClient:
    def __init__(self, model):
        self.model = model
        self.client = OpenAI(
            api_key = API_KEY,
            base_url = BASE_URL
        )

    def call_llm(self, prompt: Prompt) -> (str, str):
        response = self.client.chat.completions.create(
            messages=[{
                "role": "user",
                "content": prompt.text,
                }
            ],
            model = self.model,
            stream = False
        )

        content = response.choices[0].message.content
        raw = remove_think_blocks(content)
        raw = remove_JSON_backticks(raw)

        parsed = json.loads(raw)

        return parsed

