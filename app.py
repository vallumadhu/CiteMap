import time,os
import threading
from tools.crawler import crawl_paper
from tools.db import create_collection, get_collection, push_data, query_collection, clear_data
from tools.processors import split_text, get_paper_id_from_input
from tools.llm import explain_paper, ChatBot
from tools.prompts import chatbot_system_prompt
from config import SUMMARY_DIR


def build_kb_in_background(papers, paper_id, done_event):
    try:
        collection = get_collection(paper_id)
    except:
        collection = create_collection(paper_id)

    clear_data(collection)
    all_documents = []

    for paper in papers:
        chunks = split_text(
            text=paper["text"],
            paper_id=paper["paper_id"],
            paper_name=paper["paper_name"]
        )
        all_documents.extend(chunks)

    push_data(collection, all_documents)
    print(f"\n[KB ready. {len(all_documents)} chunks indexed. You can now chat.]\n")
    done_event.set()


def load_pipeline(paper_id, crawl_depth=1):
    paper_url = f"https://arxiv.org/pdf/{paper_id}.pdf"

    print("\nCrawling papers...")
    papers = crawl_paper(url=paper_url, crawl_depth=crawl_depth)
    print(f"Fetched {len(papers)} papers")

    print("\nGenerating summary...\n")
    response = explain_paper(papers[0]["text"])
    print("SUMMARY")
    print(response)

    with open(f"{SUMMARY_DIR}/{paper_id}.txt", "w") as f:
        f.write(response)

    done_event = threading.Event()
    thread = threading.Thread(
        target=build_kb_in_background,
        args=(papers, paper_id, done_event),
        daemon=True
    )
    thread.start()
    print("\nKnowledge Base Building Started In Background\n")

    return done_event


def chatbot_pipeline(paper_id, done_event=None):
    conversation_history = []
    print("CiteMap Chatbot ready. Type 'exit' to quit.\n")

    summary = ""
    summary_path = f"{SUMMARY_DIR}/{paper_id}.txt"
    if os.path.exists(summary_path):
        with open(summary_path) as f:
            summary = f.read()
    


    while True:
        query = input("You: ").strip()

        if query.lower() == "exit":
            break
        if not query:
            continue

        if done_event and not done_event.is_set():
            print("KB still building, please wait...\n")
            done_event.wait()

        try:
            collection = get_collection(paper_id)
        except:
            print("KB not ready yet.")
            continue

        results = query_collection(collection, query, n_results=5)
        chunks = "\n".join(results["documents"][0])

        context = f"PAPER SUMMARY:\n{summary}\nRELEVANT SECTIONS:\n{chunks}"

        output = ChatBot(
            prompt=query,
            system_prompt=chatbot_system_prompt,
            conversation_history=conversation_history,
            context=context
        )

        response = output["response"]
        conversation_history = output["history"]
        print(f"\nCiteMap: {response}\n")


def main():
    print("CiteMap - Research Paper Explainer\n")

    current_paper_id = None
    done_event = None

    while True:
        print("\nOptions:")
        print("  1. Load a paper")
        print("  2. Chat about loaded paper")
        print("  3. Exit")

        choice = input("\nChoice: ").strip()

        if choice == "1":
            value = input("arXiv ID or PDF URL: ")
            paper_id = get_paper_id_from_input(value)
            depth = input("Crawl depth (default 1): ").strip()
            depth = int(depth) if depth.isdigit() else 1

            start = time.time()
            done_event = load_pipeline(paper_id, crawl_depth=depth)
            print(f"\nSummary done in {time.time() - start:.1f}s")
            current_paper_id = paper_id

        elif choice == "2":
            if not current_paper_id:
                value = input("arXiv ID or PDF URL: ")
                current_paper_id = get_paper_id_from_input(value)
            chatbot_pipeline(current_paper_id, done_event)

        elif choice == "3":
            print("Goodbye.")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()