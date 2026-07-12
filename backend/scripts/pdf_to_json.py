import pdfplumber
import re
import json

PDF_PATH = "data/raw/Bhagavad-gita-Swami-BG-Narasingha.pdf"
OUTPUT_PATH = "data/processed/gita.json"

verses = []

current_chapter = None
current_verse = None
english_lines = []

chapter_pattern = re.compile(r"Chapter\s+(\d+)")
verse_pattern = re.compile(r"VERSE\s+(\d+)")

with pdfplumber.open(PDF_PATH) as pdf:

    for page in pdf.pages:

        text = page.extract_text()

        if not text:
            continue

        lines = text.split("\n")

        for line in lines:

            line = line.strip()

            if not line:
                continue

            # Detect Chapter
            chapter_match = chapter_pattern.match(line)

            if chapter_match:
                current_chapter = int(chapter_match.group(1))
                continue

            # Detect Verse
            verse_match = verse_pattern.match(line)

            if verse_match:
                print(f"Chapter {current_chapter} Verse {verse_match.group(1)}")
                # Save previous verse
                if current_verse is not None:

                    verses.append({
                        "chapter": current_chapter,
                        "verse": current_verse,
                        "content": " ".join(english_lines).strip()
                    })

                current_verse = int(verse_match.group(1))
                english_lines = []

                continue

            # Keep only English lines
            if (
            re.match(r"^[A-Z]", line)
            or line.startswith(("The", "One", "When", "Thus", "Lord", "Sañjaya", "Arjuna", "Addressing", "Having", "O "))
            ):
                english_lines.append(line)

# Save last verse
if current_verse is not None:
    verses.append({
        "chapter": current_chapter,
        "verse": current_verse,
        "text": " ".join(english_lines).strip()
    })

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(verses, f, indent=4, ensure_ascii=False)

print(f"Extracted {len(verses)} verses.\n")

for v in verses[:10]:
    print(f"Chapter {v['chapter']} Verse {v['verse']}")

print("\nLast 20 verses:\n")

for v in verses[-20:]:
    print(f"Chapter {v['chapter']} Verse {v['verse']}")