import pandas as pd
import re

# Load the global human first names (assume lowercase, clean)
global_first_names = set(pd.read_csv("first_names_global.csv")['first_name'].str.lower().dropna())

# Non-individual keywords for Out of Scope logic
non_individual_keywords = [
    "inc", "ltd", "llc", "gmbh", "sarl", "plc", "pvt", "company", "co.", "corp", "university", "trust",
    "foundation", "group", "ngo", "club", "committee", "society", "industries", "dealers", "hospital",
    "clinic", "lab", "government", "ministry", "municipal", "board", "authority", "council", "academy",
    "enterprise", "consultancy", "solutions", "trading", "school", "association", "firm", "services",
    "export", "import", "technologies", "logistics", "estates", "realty", "stores", "international",
]

# Titles to strip
titles = r"\b(mr|mrs|ms|miss|dr|shri|smt|sir|madam|prof|hon|rev|capt)\.?\b"

def categorize_customer(name: str) -> str:
    if not isinstance(name, str) or name.strip() == "":
        return "Out of Scope"

    name_clean = re.sub(titles, "", name.strip().lower()).strip()

    # Check for non-individual keywords
    if any(keyword in name_clean for keyword in non_individual_keywords):
        return "Out of Scope"

    # Tokenize words (split by space or hyphen)
    words = re.split(r"[\s\-]+", name_clean)

    # Check if any part of name is in global human name list
    matches = [word for word in words if word in global_first_names]

    if matches:
        return "In Scope"
    else:
        return "Out of Scope"
