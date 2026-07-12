import fitz
import re
import json

doc = fitz.open("data/raw/bhagavad-gita-in-english-source-file.pdf")

data = []

chapter = None
topic = None
content = []

chapter_re = re.compile(r"^CHAPTER\s+(\d+)$")
chapter_title_re = re.compile(r"^\d+\.\s")
started = False
started = False

for page in doc:

    lines = page.get_text().split("\n")

    for line in lines:

        line = " ".join(line.strip().split())

        if not line:
            continue

        # Start parsing only from CHAPTER 1
        if line == "CHAPTER 1":
            started = True

        if not started:
            continue

        # New Chapter
        m = chapter_re.match(line)
        if m:

            if topic and content:
                data.append({
                    "chapter": chapter,
                    "topic": topic,
                    "text": " ".join(content).strip()
                })

            chapter = int(m.group(1))
            topic = None
            content = []
            continue

        # Skip chapter title
        if chapter_title_re.match(line):
            continue

        # Skip unwanted lines
        if (
            "International Gita Society" in line
            or "Bhagavad-Gita" in line
            or line.startswith("Commentary")
            or line.startswith("NOTE")
        ):
            continue

        # New topic
        if (
            len(line) < 60
            and line[0].isupper()
            and "." not in line
            and "(" not in line
            and ")" not in line
            and ":" not in line
        ):

            if topic and content:
                data.append({
                    "chapter": chapter,
                    "topic": topic,
                    "text": " ".join(content).strip()
                })

            topic = line
            content = []
            continue

        if topic:
            content.append(line)

if topic and content:
    data.append({
        "chapter": chapter,
        "topic": topic,
        "text": " ".join(content).strip()
    })

with open("data/processed/explanations.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print(len(data))