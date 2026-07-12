from app.retriever import GitaRetriever

retriever = GitaRetriever()

results = retriever.search(
    "How do I overcome attachment?"
)

for r in results:

    print(r)