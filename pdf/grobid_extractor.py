import requests
from pathlib import Path
import xml.etree.ElementTree as ET

GROBID_URL = "http://localhost:8070/api/processFulltextDocument"

def extract_tei_xml(pdf_path: str) -> str:
    """
    Sendet ein PDF an GROBID und gibt das TEI XML zurück.
    """
    pdf_file = Path(pdf_path)

    if not pdf_file.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    with pdf_file.open("rb") as f: # rb ≈ read binary
        files = {"input": (pdf_file.name, f, "application/pdf")} # GROBID expected value <input type="file" name="input">
        response = requests.post(GROBID_URL, files=files)

    if response.status_code != 200:
        raise RuntimeError(
            f"GROBID request failed: {response.status_code}\n{response.text}"
        )

    return response.text



#############################################
NS = {"tei": "http://www.tei-c.org/ns/1.0"}

def get_text(element):
    if element is None:
        return None

    return "".join(element.itertext()).strip() # adds text elements from outer to inner nodes, concatenates and strips of whitespaces



# def extract_paper_data(tei_xml: str) -> dict:
#     root = ET.fromstring(tei_xml) # converts string into tree and returns root
#     # Title
#     title_el = root.find(".//tei:titleStmt/tei:title", NS) # . means search node start from current node (root) // search anywhere below (recursive search) tei:titleStmt /tei:title inside it, find a direct child title find a titleStmt element in the TEI namespace
#     title = get_text(title_el)
#
#     # Abstract
#     abstract_el = root.find(".//tei:abstract", NS)
#     abstract = get_text(abstract_el)
#
#     # Authors (clean full names)
#     authors = []
#     author_elements = root.findall(
#         ".//tei:teiHeader//tei:sourceDesc//tei:biblStruct//tei:analytic//tei:author",
#         NS
#     )
#
#     for author in author_elements:
#         forenames = author.findall(".//tei:forename", NS)
#         surname = author.find(".//tei:surname", NS)
#         name_parts = [f.text for f in forenames if f is not None]
#         if surname is not None:
#             name_parts.append(surname.text)
#         full_name = " ".join(name_parts).strip()
#         if full_name:
#             authors.append(full_name)
#
#     # arXiv ID
#     arxiv_el = root.find(".//tei:idno[@type='arXiv']", NS)
#     arxiv_id = get_text(arxiv_el)
#
#     return {
#         "title": title,
#         "abstract": abstract,
#         "authors": authors,
#         "arxiv_id": arxiv_id,
#     }


def extract_paper_data(pdf_path: str) -> dict:
    # all sections from abstract to conclusion/limitation
    tei_xml = extract_tei_xml(pdf_path)
    root = ET.fromstring(tei_xml)

    # Title
    title_el = root.find(".//tei:titleStmt/tei:title", NS)
    title = get_text(title_el)

    # Full body text (all sections, no tables/figures)
    body = root.find(".//tei:body", NS)
    sections = []

    STOP_SECTIONS = {"conclusion", "conclusions", "limitations", "limitation"}

    last_stop_idx = None
    all_divs = body.findall(".//tei:div", NS) if body is not None else []

    for i, div in enumerate(all_divs):
        head = div.find("tei:head", NS)
        section_title = get_text(head) if head is not None else ""
        if section_title.lower().strip() in STOP_SECTIONS:
            last_stop_idx = i

    # slice up to and including the last stop section
    if last_stop_idx is not None:
        all_divs = all_divs[:last_stop_idx + 1]

    for div in all_divs:
        head = div.find("tei:head", NS)
        section_title = get_text(head) if head is not None else ""

        paragraphs = []
        for p in div.findall("tei:p", NS):
            text = get_text(p)
            if text:
                paragraphs.append(text)

        if paragraphs:
            sections.append({
                "section": section_title,
                "text": " ".join(paragraphs)
            })

    abstract_el = root.find(".//tei:abstract", NS)
    abstract = get_text(abstract_el)

    return {
        "title": title,
        "abstract": abstract,
        "sections": sections,
    }

