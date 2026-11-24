# DocMind - Chat with your documents

Upload a PDF, Word or text file. DocMind summarizes it and answers questions,
and every answer shows the pages it came from (RAG: Retrieval-Augmented Generation).

## Setup (Windows, PowerShell, inside the folder that contains main.py)
```
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -r requirements-ml.txt
```
`requirements-ml.txt` (ChromaDB + Sentence-Transformers) is optional: if it fails to
install, DocMind automatically uses TF-IDF search and an in-memory store.

## Optional: connect Claude
Copy `.env.example` to `.env` and put your `ANTHROPIC_API_KEY` in it.
Without a key the app runs in offline mode.

## Run
```
python -m streamlit run streamlit_app.py
```
Command-line test: `python main.py data\sample_docs\college_handbook.pdf "What is the minimum attendance?"`

Tests: `pytest`

## Structure
| Path | Purpose |
|---|---|
| streamlit_app.py | Web interface |
| main.py | Command-line test |
| app/config.py | Settings |
| app/loader.py | Read PDF/DOCX/TXT page by page |
| app/chunker.py | Split into overlapping chunks |
| app/embedder.py | Embeddings (Sentence-Transformers, TF-IDF fallback) |
| app/retriever.py | Vector search (ChromaDB, NumPy fallback) |
| app/llm.py | Claude API connection |
| app/qa.py | Question answering with sources |
| app/summarizer.py | Document summaries |
| app/text_utils.py | Sentence/keyword helpers |
| tests/ | Automated tests |
| docs/ | Project report and presentation guide |
