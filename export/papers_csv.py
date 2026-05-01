from typing import List
from pathlib import Path
import csv

def export_to_csv(all_extracted_papers: List, output_path: Path) -> None:
    response_keys = []
    for entry in all_extracted_papers:
        for result in entry["results"]:
            for key in result["response"].keys():
                if key not in response_keys:
                    response_keys.append(key)

    fieldnames = ["paper", "model"] + response_keys

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for entry in all_extracted_papers:
            for result in entry["results"]:
                writer.writerow({
                    "paper": entry["paper"],
                    "model": result["model"],
                    **result["response"]
                })