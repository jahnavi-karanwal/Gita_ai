import json
import faiss
from sentence_transformers import SentenceTransformer

# ----------------------------
# Load Model
# ----------------------------
model = SentenceTransformer("BAAI/bge-small-en-v1.5")

# ----------------------------
# Load FAISS
# ----------------------------
index = faiss.read_index("data/embeddings/faiss.index")

with open("data/embeddings/metadata.json", "r", encoding="utf-8") as f:
    metadata = json.load(f)

print(f"Loaded {index.ntotal} vectors.")

while True:

    query = input("\nAsk: ")

    if query.lower() in ["exit", "quit"]:
        break

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    scores, indices = index.search(query_embedding, 5)

    print("\nTop Results\n")

    for score, idx in zip(scores[0], indices[0]):

        item = metadata[idx]

        print("=" * 60)
        print(f"Similarity : {score:.3f}")
        print(f"Type       : {item['type']}")

        if item["type"] == "verse":
            print(f"Chapter {item['chapter']} Verse {item['verse']}")
        else:
            print(f"Chapter {item['chapter']}")
            print(f"Topic : {item['topic']}")

        print()
        print(item["text"][:700])
        print()