import re
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

def split_text(text,paper_id=None,paper_name=None):

    documents = splitter.create_documents([text])
    if paper_id is not None:
        for doc in documents:
            doc.metadata["paper_id"] = paper_id

    if paper_name is not None:
        for doc in documents:
            doc.metadata["paper_name"] = paper_name

    return documents
    


def parse_arxiv_id(text):
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'\s+', ' ', text)

    arxiv_ids = re.findall(
        r'arXiv\s*[:\.]?\s*([0-9]{4}\.[0-9]{4,5})(?:v\d+)?',
        text,
        flags=re.IGNORECASE
    )
    
    seen = set()
    results = []
    for arxiv_id in arxiv_ids:
        if arxiv_id not in seen:
            seen.add(arxiv_id)
            results.append(arxiv_id)

    return results