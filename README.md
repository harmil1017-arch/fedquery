# FedQuery — FOMC Q&A with citations and evaluation

FedQuery is a small retrieval-augmented generation (RAG) app over six official Federal Open Market Committee statements. It retrieves statement paragraphs with Chroma + `all-MiniLM-L6-v2`, then asks an LLM to answer only from the retrieved passages.

## What it does

- Stores paragraph-level metadata: meeting date and paragraph number.
- Retrieves the top 2 or top 4 matching paragraphs.
- Requires citations in the format `[YYYY-MM-DD ¶N]`.
- Returns `Not found in the documents` when the answer is unsupported.
- Runs a hand-written 15-question evaluation set: 12 answerable and 3 unanswerable.

## Setup

```bash
git clone <YOUR_GITHUB_REPO_URL>
cd fedquery
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
cp .env.example .env
```

Put your API key in `.env` locally. Never commit that file. The OpenAI Python SDK reads `OPENAI_API_KEY` from your environment, so load it before commands:

```bash
export $(grep -v '^#' .env | xargs)  # macOS/Linux
python download_statements.py
python ingest.py
streamlit run app.py
```

The sources are the six latest published statements listed on the [Federal Reserve FOMC calendar](https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm). Check the Fed website policies/reuse terms before redistributing altered copies.

## Evaluation

```bash
python run_eval.py
```

Open `results.csv`. For each of the 30 runs, mark `answer_correct` and `declined_correctly` as `TRUE` or `FALSE`. Then put your final results below.

| Retrieval setting | Right source in results | Correct answers | Correct declines |
|---|---:|---:|---:|
| Top 2 | 50.0% | 8/12 | 2/3 |
| Top 4 | 91.7% | 11/12 | 1/3 |git init

## Deploy on Streamlit Community Cloud

1. Push this folder to a public GitHub repository.
2. In Streamlit Community Cloud, choose the repository and set the main file to `app.py`.
3. In **Advanced settings → Secrets**, add:
   ```toml
   OPENAI_API_KEY = "your-key-here"
   OPENAI_MODEL = "gpt-4.1-mini"
   ```
4. Deploy. Add the resulting public URL and a screenshot here.

## Resume bullets

- Built a retrieval-augmented Q&A app over six FOMC statements that gives paragraph-level citations and declines unsupported questions.
- Wrote a 15-question evaluation set and compared top-2 vs. top-4 retrieval; retrieval hit rate was **[X]% vs. [Y]%**.
- Deployed publicly with Streamlit.

**Tech:** Python, ChromaDB, sentence-transformers, Streamlit, OpenAI API
