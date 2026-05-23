from tools.crawler import download_paper,crawl_paper
from tools.db import create_collection,get_collection,push_data,query_collection
from tools.processors import split_text,parse_arxiv_id







def paper_extraction_pipeline(paper_id):

    paper_url = f"https://arxiv.org/pdf/{paper_id}.pdf"
    
    data = crawl_paper(paper_url,crawl_depth=2)
    
    print(f"Extracted {len(data)} papers.")


paper_extraction_pipeline("1505.04597")