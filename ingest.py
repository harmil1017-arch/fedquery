"""Embed statement paragraphs in a local persistent Chroma collection."""
from pathlib import Path
import re
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

DATA_DIR = Path("data/statements")
DB_DIR = "chroma_db"
COLLECTION = "fomc_statements"
embedding_fn = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

def statement_paragraphs(path: Path):
    date = path.stem
    text = path.read_text(encoding="utf-8")
    # The first two lines are provenance, not content for retrieval.
    body = text.split("\n\n", 1)[1] if "\n\n" in text else text
    return date, [re.sub(r"\s+", " ", p).strip() for p in body.split("\n\n") if p.strip()]

client = chromadb.PersistentClient(path=DB_DIR)
client.delete_collection(COLLECTION) if COLLECTION in [c.name for c in client.list_collections()] else None
collection = client.create_collection(name=COLLECTION, embedding_function=embedding_fn)

ids, documents, metadatas = [], [], []
for path in sorted(DATA_DIR.glob("*.txt")):
    date, paragraphs = statement_paragraphs(path)
    for number, paragraph in enumerate(paragraphs, start=1):
        ids.append(f"{date}-p{number}")
        documents.append(paragraph)
        metadatas.append({"meeting_date": date, "paragraph": number, "source_file": path.name})

if not ids:
    raise SystemExit("No text files found. Run: python download_statements.py")
collection.add(ids=ids, documents=documents, metadatas=metadatas)
print(f"Indexed {len(ids)} paragraphs from {len(set(m['meeting_date'] for m in metadatas))} statements.")

