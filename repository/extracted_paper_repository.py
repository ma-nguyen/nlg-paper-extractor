from pathlib import Path
from typing import List
import json
from llm.llm_client import LLMClient
from prompts.prompt import Prompt
from config import MODELS, OUTPUT_PATH

def load_extracted_papers() -> List[dict]:
    all_entries = [] # TODO outsource
    if OUTPUT_PATH.exists():
        try:
            with open(OUTPUT_PATH, "r") as f:
                content = f.read().strip()
                if content:
                    data = json.loads(content)
                    all_entries = data if isinstance(data, list) else []
        except json.JSONDecodeError:
            all_entries = []

    return all_entries
def format_paper(paper: dict) -> dict: # EXPLAIN
    sections = "\n\n".join(
        f"{s['section']}:\n{s['text']}"
        for s in paper["sections"]
    )
    return {
        "extracted_paper_text": f"Title: {paper['title']}\n\nAbstract: {paper['abstract']}\n\n{sections}"
    }
def get_missing_models(entry: dict | None, all_models: List) -> List:
    if entry is None:
        return all_models
    extracted_models = {r["model"] for r in entry["results"]}
    return [m for m in all_models if m not in extracted_models]

def run_models(prompt: Prompt, missing_models: List) -> List:
    model_results = []
    for model in missing_models:
        client = LLMClient(model)
        response = client.call_llm(prompt)
        model_results.append({"model": model, "response": response})
    return model_results

def add_extracted_paper(all_extracted_papers: List, extracted_paper: dict) -> None:
    title = extracted_paper["title"]
    existing = next((e for e in all_extracted_papers if e["paper"] == title), None)
    missing_models = get_missing_models(existing, MODELS)

    if not missing_models:
        print(f"Skipping \"{title}\" — already extracted")
        return

    prompt = Prompt("prompt_template.txt", format_paper(extracted_paper))
    model_results = run_models(prompt, missing_models)

    if existing:
        existing["results"].extend(model_results)
    else:
        all_extracted_papers.append({"paper": title, "results": model_results})

    with open(OUTPUT_PATH, "w") as f:
        json.dump(all_extracted_papers, f, indent=2)