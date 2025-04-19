import streamlit as st
import pandas as pd
import os
from io import BytesIO
from names_dataset import NameDataset

# Load name database with caching
@st.cache_resource
def load_name_dataset():
    return NameDataset(load_first_names=True, load_last_names=True)
nd = load_name_dataset()

# Expanded non-individual keywords for global coverage
non_individual_keywords = [
    # Legal/Corporate Structures (Global)
    "inc", "inc.", "llc", "l.l.c.", "ltd", "ltd.", "limited", "corp", "corporation", "co", "co.", "pte", "pvt", "llp",
    "gmbh", "ag", "nv", "bv", "kk", "oy", "ab", "plc", "s.a", "s.a.s", "sa", "sarl", "sl", "aps", "as", "kft", "pt", "sdn", "bhd",
    "srl", "pty ltd", "se", "a/s", "sp zoo", "eurl",
    # Pharmacy/Healthcare (Global)
    "pharmacy", "drugstore", "healthcare", "medical", "clinic", "hospital", "apothecary", "dispensary",
    # Academic/Institutional
    "university", "uni", "institute", "inst", "college", "academy", "school", "faculty", "dept", "department",
    # Science/R&D
    "centre", "center", "r&d", "science", "biotech", "medtech", "ai",
    # Government/NGO
    "govt", "government", "ngo", "ministry", "agency",
    # Professional Services
    "solutions", "consulting", "partners", "services", "group",
    # Retail/Media
    "store", "shop", "outlet", "market",
    # Others
    "foundation", "trust", "association"
]

# Enhanced name classification logic
def classify_name(name):
    try:
        name = str(name).strip().lower()
        name_parts = name.split()

        # Check for non-individual keywords
        for keyword in non_individual_keywords:
            if keyword in name:
                return "Out of Scope"

        # Check if it's an individual name using NameDataset
        if len(name_parts) >= 1:
            first_word = name_parts[0]
            last_word = name_parts[-1] if len(name_parts) > 1 else None
            first_result = nd.search(first_word)
            last_result = nd.search(last_word) if last_word else {'last_name': None}

            if (first_result.get('first_name') or last_result.get('last_name')) and not any(kw in name for kw in non_individual_keywords):
                return "In Scope"
            elif not first_result.get('first_name') and not last_result.get('last_name') and any(kw in name for kw in non_individual_keywords):
                return "Out of Scope"
            else:
                return "Needs Review"  # For ambiguous cases
    except Exception as e:
        st.error(f"Error in classification: {e}")
        return "Needs Review"
    return "Out of Scope"

# UI setup
st.set_page_config(page_title="Customer Categorization AI", layout="centered")
st.title("🧠 Ultra Accurate Customer Name Categorization")
st.markdown("This tool uses AI + Global Name Dataset to classify customers as **In Scope (Individuals)** or **Out of Scope (Companies)**.")

uploaded_file = st.file_uploader("📁 Upload your Excel or CSV file", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        ext = os.path.splitext(uploaded_file.name)[1]

        if ext == ".csv":
            df = pd.read_csv(uploaded_file)
        elif ext in [".xls", ".xlsx"]:
            df = pd.read_excel(uploaded_file)
        else:
            st.error("Unsupported file format.")
            st.stop()

        # Auto-detect name column
        name_col = None
        for col in df.columns:
            if "name" in col.lower():
                name_col = col
                break

        if not name_col:
            name_col = st.selectbox("Select the column containing customer names:", df.columns)

        st.info(f"Using column: **{name_col}** for classification")

        df["Scope Status"] = df[name_col].apply(classify_name)
        st.success("✅ Categorization Complete!")

        st.dataframe(df.head(30))

        # Downloadable result
        output = BytesIO()
        df.to_excel(output, index=False, engine='openpyxl')
        st.download_button("📥 Download Categorized File", output.getvalue(), file_name="categorized_customers.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    except Exception as e:
        st.error(f"❌ Error: {e}")
