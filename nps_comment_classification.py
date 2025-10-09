"""
NPS Comment Classification Pipeline (Zero-Shot GPT-4)
----------------------------------------------------
Description:
- Merges multiple Excel survey files
- Cleans and preprocesses open-ended NPS comments
- Classifies feedback into thematic categories using GPT-4 (zero-shot)
- Exports the enriched dataset to Excel for visualization in Power BI

Note:
    File paths and API key placeholders have been redacted for confidentiality.
"""

#import packages

import pandas as pd
import os
import glob
import re
import openai
import json
import time

# OpenAI API Key
openai.api_key = "[YOUR OPENAI API KEY]"  #replace 

# Read Data
folder_path = r"/Users/[USERNAME]/Documents/[PROJECT_FOLDER]/" #replace
all_files = glob.glob(os.path.join(folder_path, "*.xlsx"))

dfs = []
for file in all_files:
    try:
        print(f" Load Data: {file}")
        df = pd.read_excel(file)
        df["Datei"] = os.path.basename(file)
        dfs.append(df)
    except Exception as e:
        print(f" Error in {file}: {e}")

if not dfs:
    raise ValueError("No Data loaded. Please check path again.")

df = pd.concat(dfs, ignore_index=True)

# Check columns
text_col = "answer_Y2qkC"    # Comment
score_col = "answer_4nmmE"   # NPS 

if text_col not in df.columns or score_col not in df.columns:
    raise ValueError(f"columns missing: {text_col} or {score_col}")

df = df.dropna(subset=[score_col])
df[score_col] = df[score_col].astype(int)
df[text_col] = df[text_col].fillna("").astype(str)

# Text cleaning
def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\d+", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

df['Text_Cleaned'] = df[text_col].apply(clean_text)

# OpenAI Prompt
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

# Classification function
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
        attributes = json_result.get("attributes", ["Keine Angabe"]) # Default if key missing

        # Max 3 entries
        attributes = attributes[:3]
        # If less than 3, entries filled with "None"
        attributes += [None] * (3 - len(attributes))

        return attributes

    except Exception as e:
        print(f" Error at text: {comment_text[:50]}... {e}")
        return ["Error", None, None]

# Text classification
results = []
for i, text in enumerate(df["Text_Cleaned"]):
    print(f"Classified row {i+1}/{len(df)}")
    result = classify_comment(text)
    results.append(result)
    time.sleep(0.3)                 # insert pause to avoid rate limits

# Append columns to dataframe
normalized_results = []
for row in results:
    row = row[:3]                   # max 3 elements
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

# Join Dataframe
df = pd.concat([df, results_df], axis=1)

# Export Dataframe
output_path = r"/Users/[USERNAME]/Documents/[PROJECT_FOLDER]/Kommentare_Clustering.xlsx"    #replace
df.to_excel(output_path, index=False)
print(f" Data saved: {output_path}")
