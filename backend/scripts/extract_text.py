import fitz

doc = fitz.open("data/raw/Bhagavad-gita-Swami-BG-Narasingha.pdf")

text = ""

for page in doc:
    text += page.get_text("text") + "\n"

with open("data/raw/extracted_text.txt", "w", encoding="utf-8") as f:
    f.write(text)

print("Done")