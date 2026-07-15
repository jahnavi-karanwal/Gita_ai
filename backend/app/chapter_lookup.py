import json
import re


class ChapterLookup:

    def __init__(self):

        with open("data/processed/gita.json", "r", encoding="utf-8") as f:
            self.verses = json.load(f)

    def find(self, query):

        q = query.lower().strip()

        print("\n==========================")
        print("CHAPTER LOOKUP")
        print("Original :", query)

        # ------------------------------------
        # Ignore verse queries
        # ------------------------------------

        if "verse" in q or ":" in q or "." in q:
            print("Looks like a verse query.")
            print("==========================\n")
            return None

        # ------------------------------------
        # Match:
        # chapter 2
        # chap 2
        # chp 2
        # ch 2
        # ------------------------------------

        patterns = [
            r"(?:chapter|chap|chp|ch)\s*#?\s*(\d+)"
        ]

        chapter = None

        for pattern in patterns:

            match = re.search(pattern, q)

            if match:
                chapter = int(match.group(1))
                break

        if chapter is None:

            print("Chapter not found.")
            print("==========================\n")
            return None

        # ------------------------------------
        # Bhagavad Gita has only 18 chapters
        # ------------------------------------

        if chapter < 1 or chapter > 18:

            print(f"Invalid chapter: {chapter}")
            print("==========================\n")
            return None

        print(f"Looking for Chapter {chapter}")

        # ------------------------------------
        # Collect all verses
        # ------------------------------------

        chapter_verses = [

            verse

            for verse in self.verses

            if verse["chapter"] == chapter
        ]

        if len(chapter_verses) == 0:

            print("Chapter exists but contains no verses.")
            print("==========================\n")

            return None

        print(
            f"Found {len(chapter_verses)} verses in Chapter {chapter}"
        )

        print("==========================\n")

        return chapter_verses