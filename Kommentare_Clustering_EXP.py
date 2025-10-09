import pandas as pd
import os
import glob
import re
import openai
import json
import time

# -------------------------
# OPENAI API-KEY
# -------------------------
openai.api_key = "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"   

# -------------------------
# DATEIEN EINLESEN
# -------------------------
folder_path = r"C:\Users\viviane.lorenc\OneDrive - DuMont Systems GmbH & Co. KG\Dokumente - Teamkanal\PowerBI\NPS\Cleverpush Antworten\Express"
all_files = glob.glob(os.path.join(folder_path, "*.xlsx"))

dfs = []
for file in all_files:
    try:
        print(f" Lade Datei: {file}")
        df = pd.read_excel(file)
        df["Datei"] = os.path.basename(file)
        dfs.append(df)
    except Exception as e:
        print(f" Fehler in {file}: {e}")

if not dfs:
    raise ValueError("Keine Dateien geladen. Bitte Pfad prüfen.")

df = pd.concat(dfs, ignore_index=True)

# -------------------------
# SPALTEN PRÜFEN
# -------------------------
text_col = "answer_Y2qkC"    # Kommentar
score_col = "answer_4nmmE"   # NPS-Wert

if text_col not in df.columns or score_col not in df.columns:
    raise ValueError(f"Spalten fehlen: {text_col} oder {score_col}")

df = df.dropna(subset=[score_col])
df[score_col] = df[score_col].astype(int)
df[text_col] = df[text_col].fillna("").astype(str)

# -------------------------
# TEXT CLEANING
# -------------------------
def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\d+", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

df['Text_Cleaned'] = df[text_col].apply(clean_text)

# -------------------------
# PROMPT FÜR OPENAI
# -------------------------
categories = [
    "Technik / App",
    "Politische Haltung",
    "Kosten / Preis",
    "Fake News / Missvertrauen",
    "Aktualität / Tagesgeschehen",
    "Regionale Inhalte",
    "Design / Bedienung",
    "Qualität / Journalismus",
    "Werbung",
    "Keine Angabe",
]

system_prompt = f"""
You are a text classification assistant.

Your task is to analyze a user's comment and identify its main themes. Based on the content of the text, return a JSON object with a single key called "attributes". The value of this key should be a list containing 1 to 3 strings, each representing a broad category that best describes the user's comment.

Only choose from the following predefined categories:
{json.dumps(categories, indent=4)}

If the comment is unclear or unspecific, pick the category that fits best instead of "Keine Angabe".

Return strictly JSON, no explanation.
"""

# -------------------------
# FUNKTION FÜR EINEN TEXT
# -------------------------
def classify_comment(comment_text):
    if not comment_text.strip():
        return ["Keine Angabe", None, None]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": comment_text}
            ],
            temperature=0,
            max_tokens=150
        )
        raw_output = response.choices[0].message.content
        json_result = json.loads(raw_output)
        attributes = json_result.get("attributes", ["Keine Angabe"])

        # Immer maximal 3 Einträge behalten
        attributes = attributes[:3]
        # Falls weniger als 3, mit None auffüllen
        attributes += [None] * (3 - len(attributes))

        return attributes

    except Exception as e:
        print(f" Fehler bei Text: {comment_text[:50]}... {e}")
        return ["Fehler", None, None]

# -------------------------
# ALLE TEXTE KLASSIFIZIEREN
# -------------------------
results = []
for i, text in enumerate(df["Text_Cleaned"]):
    print(f"→ Klassifiziere Zeile {i+1}/{len(df)}")
    result = classify_comment(text)
    results.append(result)
    time.sleep(0.3)    # kleine Pause, um Rate Limits zu vermeiden

# -------------------------
# SPALTEN ANZAHL KORRIGIEREN
# -------------------------
normalized_results = []
for row in results:
    row = row[:3]                        # max. 3 Elemente
    while len(row) < 3:
        row.append(None)
    normalized_results.append(row)

results_df = pd.DataFrame(
    normalized_results,
    columns=[
        "ZeroShot_Kategorie_1",
        "ZeroShot_Kategorie_2",
        "ZeroShot_Kategorie_3"
    ]
)

# -------------------------
# DATAFRAME ZUSAMMENFÜGEN
# -------------------------
df = pd.concat([df, results_df], axis=1)

# -------------------------
# EXPORTIEREN
# -------------------------
output_path = r"C:\Users\viviane.lorenc\OneDrive - DuMont Systems GmbH & Co. KG\Dokumente - Teamkanal\PowerBI\NPS\Python Skripts\Kommentare Clustering\Kommentare_Clustering_EXP.xlsx"
df.to_excel(output_path, index=False)
print(f" Analyse abgeschlossen! Datei gespeichert unter: {output_path}")
