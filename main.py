from pathlib import Path
from pdf.grobid_extractor import extract_paper_data
from repository.extracted_paper_repository import load_extracted_papers, add_extracted_paper
from config import PAPER_DIR, OUTPUT_CSV_PATH, OUTPUT_HTML_PATH
from export.papers_csv import export_to_csv
from export.papers_html import export_to_html

# TODO
# X clean minimal implementation
# X format JSON with respective model
# X 3 LLMs calls into 1 JSON entry -> LOOP
# X scalable adaptive architecture
# X give full paper
# X Iterate over set of papers with model names
# X when processing several papers - intermediate savepoints
# X if paper already extracted continue
# X Minimize
# X LLM call with model name
# X BASE DIR centralized
# X Prompt-Input
# X CSV export
# X Excel Import
# X Clean HTML overview of papers
# GitHub Upload
# Clean Architecture
# DocString
# comments
# add paper extraction successful for each new paper extracted
# add sum of successfully new extracted papers

def main():
    all_extracted_papers = load_extracted_papers()

    for paper_path in Path(PAPER_DIR).glob("*.pdf"):
        paper = extract_paper_data(paper_path)
        add_extracted_paper(all_extracted_papers, paper)

        break # Debugging for only 1 paper

    export_to_csv(all_extracted_papers, OUTPUT_CSV_PATH)
    export_to_html(all_extracted_papers, OUTPUT_HTML_PATH)

if __name__ == "__main__":
    main()