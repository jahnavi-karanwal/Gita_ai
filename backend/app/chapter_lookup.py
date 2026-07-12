import json
import re


class ChapterLookup:

    def __init__(self):
        with open("data/processed/gita.json", "r", encoding="utf-8") as f:
            self.verses = json.load(f)

    def find(self, query):

        q = query.lower().strip()
        replacements = {
        "chp": "chapter",
        "chap": "chapter",
        "ch ": "chapter ",
        }

        for old, new in replacements.items():
            q = q.replace(old, new)

        if "verse" in q or ":" in q or "." in q:
            return None

        patterns = [
            r"chapter\s+(\d+)",
            r"chap\s+(\d+)",
            r"ch\s+(\d+)"
        ]

        chapter = None

        for pattern in patterns:

            match = re.search(pattern, q)

            if match:
                chapter = int(match.group(1))
                break

        if chapter is None:
            return None

        chapter_verses = [
            verse
            for verse in self.verses
            if verse["chapter"] == chapter
        ]

        if len(chapter_verses) == 0:
            return None

        return chapter_verses