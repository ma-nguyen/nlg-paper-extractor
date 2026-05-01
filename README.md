# NLG Paper Extractor

A pipeline that extracts structured metadata from NLG research papers using multiple LLMs in parallel. Papers are parsed from PDF via GROBID, fed into configurable prompt templates, and results are saved as JSON with automatic checkpointing.

---

## What it does

- Extracts full text from PDF papers using GROBID
- Runs multiple LLMs on each paper using a configurable prompt template
- Saves results per paper and per model as structured JSON
- Skips already-processed papers and fills in missing model responses on re-runs
- Exports results to CSV and HTML for human review

---

## Requirements

- Python 3.11+
- Docker (for GROBID)

---

## Setup

**1. Clone the repository:**
```bash
git clone git@github.com:ma-nguyen/nlg-paper-extractor.git
cd nlg-paper-extractor
```

**2. Create and activate a virtual environment:**
**Mac/Linux:**
```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

**Windows:**
```bash
py -3.11 -m venv .venv
.venv\Scripts\activate
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Create a `.env` file in the project root:**
```
API_KEY=your_api_key_here
```

**5. Start GROBID via Docker:**
```bash
docker run -t --rm -p 8070:8070 lfoppiano/grobid:0.8.0
```

GROBID must be running before you run the extractor.

---

## Usage

**1. Add your PDF papers to the `papers/` folder.**

**2. Run the extractor:**
```bash
python main.py
```

Results are saved incrementally to `data/` after each paper is processed. If the script is interrupted, re-running it will skip already-processed papers and only process the remaining ones.
The human readable versions in CSV for export and HTML are in ```data/``` as well. Open `[MODEL_NAMES].html` in any browser to review model outputs side by side.

---

## Project Structure

```
nlg-paper-extractor/
├── main.py                        # Entry point
├── config.py                      # Paths, models, API credentials
├── requirements.txt
├── prompt_templates/
│   └── prompt_template.txt        # Prompt with placeholders
├── pdf/
│   └── grobid_extractor.py        # PDF → structured text via GROBID
├── llm/
│   ├── llm_client.py              # LLM API calls and response parsing
│   └── postprocessing.py          # Clean up raw LLM responses
├── prompts/
│   └── prompt.py                  # Prompt builder
├── repository/
│   └── extracted_paper_repository.py  # Load, save, manage results
├── export/
│   ├── papers_csv.py              # Export results to CSV
│   └── papers_html.py             # Export results to HTML
├── services/                      # (empty)
├── data/                          # Output JSON, CSV and HTML results
└── papers/                        # Input PDF papers
```

---

## Models

Configured in `config.py`:

```python
MODELS = [
    "gpt-oss-120b",
    "deepseek-r1-distill-llama-70b",
    "qwen3-30b-a3b-instruct-2507"
]
```

Each model is called independently for every paper. Results are stored per model so individual model responses can be compared.

---

## Output Format

Results are saved as a JSON file in `data/`:

```json
[
  {
    "paper": "Paper Title",
    "results": [
      {
        "model": "gpt-oss-120b",
        "response": {
          "goal": "...",
          "findings": "..."
        }
      },
      {
        "model": "deepseek-r1-distill-llama-70b",
        "response": {
          "goal": "...",
          "findings": "..."
        }
      },
      {
        "model": "qwen3-30b-a3b-instruct-2507",
        "response": {
          "goal": "...",
          "findings": "..."
        }
      }
    ]
  }
]
```

---

## Prompt Templates

Prompt templates are stored in `prompt_templates/` and use Python-style placeholders:

```
{extracted_paper_text}
```

To use a different prompt, add a new `.txt` file to `prompt_templates/` and update the filename in `config.py`. The placeholders must match the keys returned by `format_paper()`.
