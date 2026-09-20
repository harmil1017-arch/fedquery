"""Run retrieval at k=2 and k=4, then write a CSV for manual answer marking."""
import csv, json
from fedquery import retrieve, answer

questions = json.load(open("eval_questions.json", encoding="utf-8"))
rows = []
for top_k in (2, 4):
    for item in questions:
        passages = retrieve(item["question"], top_k)
        retrieved_ids = [p["id"] for p in passages]
        hit = item["source_id"] in retrieved_ids if item["answerable"] else "n/a"
        result = answer(item["question"], top_k)
        rows.append({
            "top_k": top_k, "id": item["id"], "question": item["question"],
            "answerable": item["answerable"], "expected_answer": item["expected_answer"],
            "expected_source": item["source_id"], "retrieved_ids": "; ".join(retrieved_ids),
            "retrieval_hit": hit, "model_answer": result["answer"],
            "answer_correct": "MARK_ME", "declined_correctly": "MARK_ME"
        })

with open("results.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader(); writer.writerows(rows)

for top_k in (2, 4):
    subset = [r for r in rows if r["top_k"] == top_k and r["answerable"]]
    hits = sum(r["retrieval_hit"] is True for r in subset)
    print(f"top-{top_k}: retrieval hit rate = {hits}/{len(subset)} ({hits / len(subset):.1%})")
print("Wrote results.csv. Fill answer_correct and declined_correctly, then summarize manually.")

