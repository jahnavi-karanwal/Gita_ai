import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# ======================================================
# Paths
# ======================================================

GITA_PATH = "data/processed/gita.json"
EXPLANATION_PATH = "data/processed/explanations.json"

INDEX_PATH = "data/embeddings/faiss.index"
METADATA_PATH = "data/embeddings/metadata.json"

# ======================================================
# Load Embedding Model
# ======================================================

print("Loading embedding model...")

model = SentenceTransformer("BAAI/bge-small-en-v1.5")

documents = []
metadata = []

# ======================================================
# Load Gita Verses
# ======================================================

print("Loading verses...")

with open(GITA_PATH, "r", encoding="utf-8") as f:
    verses = json.load(f)

for verse in verses:

    text = verse["content"]

    document = (
        f"Bhagavad Gita\n"
        f"Chapter {verse['chapter']}\n"
        f"Verse {verse['verse']}\n\n"
        f"{text}"
    )

    documents.append(document)

    metadata.append({
        "type": "verse",
        "chapter": verse["chapter"],
        "verse": verse["verse"],
        "topic": None,
        "text": text
    })

# ======================================================
# Load Explanations
# ======================================================

print("Loading explanations...")

with open(EXPLANATION_PATH, "r", encoding="utf-8") as f:
    explanations = json.load(f)

for exp in explanations:

    document = (
        f"Bhagavad Gita\n"
        f"Chapter {exp['chapter']}\n"
        f"{exp['topic']}\n\n"
        f"{exp['text']}"
    )

    documents.append(document)

    metadata.append({
        "type": "explanation",
        "chapter": exp["chapter"],
        "verse": None,
        "topic": exp["topic"],
        "text": exp["text"]
    })

print(f"\nTotal Documents: {len(documents)}")

# ======================================================
# Generate Embeddings
# ======================================================

print("\nGenerating embeddings...")

embeddings = model.encode(
    documents,
    convert_to_numpy=True,
    normalize_embeddings=True,
    show_progress_bar=True
)

embeddings = embeddings.astype(np.float32)

# ======================================================
# Build FAISS Index
# ======================================================

dimension = embeddings.shape[1]

index = faiss.IndexFlatIP(dimension)
index.add(embeddings)

# ======================================================
# Save
# ======================================================

faiss.write_index(index, INDEX_PATH)

with open(METADATA_PATH, "w", encoding="utf-8") as f:
    json.dump(metadata, f, indent=4, ensure_ascii=False)

# ======================================================
# Summary
# ======================================================

print("\n" + "=" * 50)
print("Embedding Complete")
print("=" * 50)
print(f"Documents : {len(documents)}")
print(f"Vectors   : {index.ntotal}")
print(f"Dimension : {dimension}")
print(f"Index     : {INDEX_PATH}")
print(f"Metadata  : {METADATA_PATH}")
print("=" * 50)