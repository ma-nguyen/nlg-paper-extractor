import re

def remove_think_blocks(text: str) -> str:
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()

def remove_JSON_backticks(text: str) -> str:
    # Markdown-Fences entfernen (```json ... ```)
    if text.startswith("```"):
        text = text[text.find("\n") + 1:]
        text = text[:text.rfind("```")].strip()

    return text