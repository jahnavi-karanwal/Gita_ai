import json
import re


class VerseLookup:

    def __init__(self):

        with open("data/processed/gita.json", "r", encoding="utf-8") as f:
            self.verses = json.load(f)

    def find(self, query):

        q = query.lower().strip()

        # ------------------------------------
        # Normalize common abbreviations
        # ------------------------------------

        

        print("\n==========================")
        print("VERSE LOOKUP")
        print("Original :", query)
        print("Normalized:", q)

        chapter = None
        verse = None

        # ------------------------------------
        # chapter X verse Y
        # ------------------------------------

        m = re.search(
            r"(?:chapter|chap|chp|ch)\s*#?\s*(\d+)\s+verse\s+(\d+)",
            q,
        )

        if m:
            chapter = int(m.group(1))
            verse = int(m.group(2))

        # ------------------------------------
        # verse Y of chapter X
        # ------------------------------------

        elif m := re.search(
            r"verse\s+(\d+)\s+of\s+chapter\s*#?\s*(\d+)",
            q,
        ):
            verse = int(m.group(1))
            chapter = int(m.group(2))

        # ------------------------------------
        # BG X:Y
        # ------------------------------------

        elif m := re.search(
            r"bg\s*(\d+):(\d+)",
            q,
        ):
            chapter = int(m.group(1))
            verse = int(m.group(2))

        # ------------------------------------
        # X:Y
        # ------------------------------------

        elif m := re.search(
            r"\b(\d+):(\d+)\b",
            q,
        ):
            chapter = int(m.group(1))
            verse = int(m.group(2))

        # ------------------------------------
        # X.Y
        # ------------------------------------

        elif m := re.search(
            r"\b(\d+)\.(\d+)\b",
            q,
        ):
            chapter = int(m.group(1))
            verse = int(m.group(2))

        # ------------------------------------
        # No match
        # ------------------------------------

        if chapter is None:

            print("No verse pattern matched.")
            print("==========================\n")

            return None

        print(f"Looking for Chapter {chapter}, Verse {verse}")

        # ------------------------------------
        # Search dataset
        # ------------------------------------

        for item in self.verses:

            if (
                item.get("chapter") == chapter
                and item.get("verse") == verse
            ):

                print("FOUND VERSE")
                print("==========================\n")

                return {
                    "chapter": item["chapter"],
                    "verse": item["verse"],
                    "content": item.get("content") or item.get("text"),
                }

        print("Verse NOT FOUND in dataset.")
        print("==========================\n")

        return None