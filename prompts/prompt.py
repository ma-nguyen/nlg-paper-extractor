from langchain_core.prompts import PromptTemplate
from config import PROMPT_TEMPLATE_DIR

class Prompt: # TODO more adjustable
    def __init__(self, prompt_template: str, values: dict):
        # prompt_template_path = PROMPT_TEMPLATE_DIR / prompt_template
        #
        # with open(prompt_template_path, "r", newline="") as prompt_file:
        #     prompt_template = prompt_file.read().replace('\n', '')
        # prompt_template = PromptTemplate.from_template(prompt_template)
        #
        # formated_values = format_paper(values)
        # self.text = prompt_template.format(**formated_values)

        prompt_template_path = PROMPT_TEMPLATE_DIR / prompt_template

        with open(prompt_template_path, "r") as prompt_file:
            template = prompt_file.read()

        self.text = template.format(**values)
