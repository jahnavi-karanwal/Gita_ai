def format_context(results):

    context = ""

    for item in results:

        if item["type"] == "verse":

            context += (
                f"\n[Verse]\n"
                f"Chapter {item['chapter']} Verse {item['verse']}\n"
                f"{item['text']}\n"
            )

        elif item["type"] == "explanation":

            context += (
                f"\n[Explanation]\n"
                f"Chapter {item['chapter']}\n"
                f"Topic: {item['topic']}\n"
                f"{item['text']}\n"
            )

    return context