import streamlit as st
import pandas as pd
import os
from io import BytesIO
import re

# Set page configuration as the first Streamlit command
st.set_page_config(page_title="Customer Categorization AI", layout="centered")

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

# Enhanced out-of-scope detection logic
def classify_name(name):
    try:
        name = str(name).strip().lower()
        # Check for non-individual keywords with regex for better matching
        for keyword in non_individual_keywords:
            if re.search(rf'\b{re.escape(keyword)}\b', name):
                return "Out of Scope"
        return "In Scope"  # Default to In Scope if no keywords match
    except Exception as e:
        st.error(f"Error in classification: {e}")
        return "Needs Review"

# UI setup and main app logic
st.title("🧠 Out-of-Scope Customer Categorization")
st.markdown("This tool identifies **Out of Scope (Non-Individuals)** like companies or institutions, with remaining as **In Scope (Individuals)**.")

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
