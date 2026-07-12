import json
import re
import pandas as pd

CSV_PATH = "data/raw/gita3.csv"
OUTPUT_PATH = "data/processed/gita.json"

df = pd.read_csv(CSV_PATH)

gita = []

for _, row in df.iterrows():

    text = str(row["EngMeaning"]).strip()

    # Remove verse prefix like:
    # 1.1
    # 1.2.
    # 18.66
    text = re.sub(r"^\d+\.\d+\.?\s*", "", text)

    # Remove newlines and extra spaces
    text = " ".join(text.split())

    gita.append({
        "chapter": int(row["Chapter"]),
        "verse": int(row["Verse"]),
        "content": text
    })

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(gita, f, indent=4, ensure_ascii=False)

print(f"Saved {len(gita)} verses to {OUTPUT_PATH}")