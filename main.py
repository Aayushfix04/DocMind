"""Command-line test for DocMind (no web page needed).

Usage:
    python main.py data/sample_docs/college_handbook.pdf
    python main.py data/sample_docs/college_handbook.pdf "What is the minimum attendance?"
"""

import sys

from app import config, llm
from app.chunker import chunk_pages
from app.embedder import Embedder
from app.loader import load_document
from app.qa import answer_question
from app.retriever import Retriever
from app.summarizer import summarize


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    path = sys.argv[1]
    question = " ".join(sys.argv[2:]).strip()

    try:
        pages = load_document(path)
    except (FileNotFoundError, ValueError) as error:
        print(f"Error: {error}")
        return

    chunks = chunk_pages(pages, config.CHUNK_SIZE, config.CHUNK_OVERLAP)
    embedder = Embedder()
    retriever = Retriever(embedder)
    retriever.build(path, chunks)

    print(f"Pages: {len(pages)} | Words: {sum(len(p['text'].split()) for p in pages)} | Chunks: {len(chunks)}")
    print(f"Embeddings: {embedder.label}")
    print(f"Vector store: {retriever.store}")
    print(f"Answer mode: {'Claude' if llm.is_available() else 'Offline'}")
    for note in (embedder.note, retriever.note):
        if note:
            print(f"Note: {note}")

    if question:
        result = answer_question(question, retriever, pages=pages, top_k=config.TOP_K)
        print(f"\nQ: {question}\n\n{result['answer']}")
        for s in result["sources"]:
            print(f"\n  [page {s['page']}, relevance {s['score']:.0%}] {s['text'][:150]}...")
    else:
        print("\n--- Summary ---")
        print(summarize(pages)["text"])


if __name__ == "__main__":
    main()
