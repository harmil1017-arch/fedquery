"""Retrieval and grounded answering for FedQuery."""
import os
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from openai import OpenAI

COLLECTION = "fomc_statements"
embedding_fn = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

def collection():
    client = chromadb.PersistentClient(path="chroma_db")
    return client.get_collection(COLLECTION, embedding_function=embedding_fn)

def retrieve(question: str, top_k: int = 4):
    result = collection().query(query_texts=[question], n_results=top_k)
    return [
        {"id": result["ids"][0][i], "text": result["documents"][0][i], "metadata": result["metadatas"][0][i]}
        for i in range(len(result["ids"][0]))
    ]

def answer(question: str, top_k: int = 4):
    passages = retrieve(question, top_k)
    context = "\n\n".join(
        f"[{p['metadata']['meeting_date']} ¶{p['metadata']['paragraph']}] {p['text']}" for p in passages
    )
    instructions = """Answer only using the supplied passages. If they do not directly answer the question, reply exactly: Not found in the documents. Otherwise give a concise answer and cite every claim as [YYYY-MM-DD ¶N]. Do not use outside knowledge."""
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(
        model=os.environ.get("OPENAI_MODEL", "gpt-4.1-mini"),
        instructions=instructions,
        input=f"Question: {question}\n\nPassages:\n{context}",
    )
    return {"answer": response.output_text.strip(), "passages": passages}

