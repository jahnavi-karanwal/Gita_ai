import json
import faiss
from sentence_transformers import SentenceTransformer


class GitaRetriever:

    def __init__(
        self,
        index_path="data/embeddings/faiss.index",
        metadata_path="data/embeddings/metadata.json",
        model_name="BAAI/bge-small-en-v1.5"
    ):

        self.model = SentenceTransformer(model_name)

        self.index = faiss.read_index(index_path)

        with open(metadata_path, "r", encoding="utf-8") as f:
            self.metadata = json.load(f)

    def search(self, query, k=5):

        embedding = self.model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        scores, indices = self.index.search(embedding, k)

        results = []

        for score, idx in zip(scores[0], indices[0]):

            item = self.metadata[idx].copy()

            item["score"] = float(score)

            results.append(item)

        return results