import requests,os
import uuid
from tools.processors import parse_arxiv_id
from config import PAPER_DIR
import fitz


def download_paper(url,name=None):
    id = str(uuid.uuid4())

    name = "paper_" if name is None else name
    name = name+"_"+id

    response = requests.get(url)
    
    os.makedirs(PAPER_DIR, exist_ok=True)
    with open(f"{PAPER_DIR}/{name}.pdf","wb") as f:
        f.write(response.content)
    
    print(f"Downloaded paper to {PAPER_DIR}/{name}.pdf")
    return f"{PAPER_DIR}/{name}.pdf"

def pdf2text(pdf_path):
    pdf = fitz.open(pdf_path)
    text = ""
    for page in pdf:
        text += page.get_text()
    return text


def extract_reference_section(text):

    markers = ["references\n", "bibliography\n"]
    last_pos = -1
    for marker in markers:
        pos = text.lower().rfind(marker)
        if pos > last_pos:
            last_pos = pos
    
    if last_pos == -1:
        return None
    
    return text[last_pos:]



def crawl_paper(url, name=None, crawl_depth=1, visited=None):

    if visited is None:
        visited = set()

    data = []

    paper_id = url.split("/")[-1].replace(".pdf", "")

    if paper_id in visited:
        return data

    visited.add(paper_id)

    downloaded_path = download_paper(url, name)

    text = pdf2text(downloaded_path)

    data.append({
        "paper_id": paper_id,
        "paper_name": name if name else paper_id,
        "text": text
    })

    if crawl_depth == 0:
        return data

    ref_section = extract_reference_section(text)

    if ref_section is None:
        return data

    arxiv_ids = parse_arxiv_id(ref_section)

    for arxiv_id in arxiv_ids:

        pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"

        child_data = crawl_paper(
            pdf_url,
            crawl_depth=crawl_depth - 1,
            visited=visited
        )
        data.extend(child_data)

    return data