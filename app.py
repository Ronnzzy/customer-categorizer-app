# Streamlit Customer Categorization App
import streamlit as st
import pandas as pd
import re
from io import BytesIO

st.set_page_config(page_title="Customer Categorizer", layout="centered")
st.title("📊 Customer Name Categorizer")
st.write("Upload your Excel file containing customer names. This tool will classify them as **Individual**, **Other**, or **Needs Review** based on name patterns and keywords.")

# --- Upload file ---
uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

# --- Keywords for 'Other' classification ---
non_individual_keywords = [
    "inc", "inc.", "llc", "l.l.c.", "ltd", "ltd.", "limited", "corp", "corporation", "co", "co.", "pte", "pvt", "llp",
    "gmbh", "ag", "nv", "bv", "kk", "oy", "ab", "plc", "s.a", "s.a.s", "sa", "sarl", "sl", "aps", "as", "kft", "pt", "sdn", "bhd",
    "university", "uni", "institute", "inst", "college", "academy", "school", "faculty", "dept", "department", "cnrs",
    "research", "laboratory", "lab", "education", "educational", "engineering", "polytechnic", "polytech",
    "centre", "center", "r&d", "science", "sciences", "technical", "technological", "technology", "innovation",
    "biotech", "medtech", "ai", "ml", "cybernetics", "govt", "government", "ngo", "n.g.o", "nonprofit", "non-profit",
    "ministry", "embassy", "consulate", "office", "admin", "administration", "secretariat", "authority", "commission",
    "agency", "bureau", "solutions", "consulting", "consultants", "advisory", "advisors", "partners", "partnership",
    "associates", "services", "ventures", "enterprises", "management", "finance", "capital", "holdings", "intl",
    "international", "global", "industries", "logistics", "trading", "procurement", "group", "store", "shop",
    "bookshop", "library", "distribution", "distributors", "outlet", "media", "publications", "books", "press",
    "foundation", "fondation", "fondazione", "trust", "union", "syndicate", "board", "chamber", "association",
    "club", "society", "network", "cooperative", "federation", "council", "committee", "coalition", "initiative",
    "team", "division", "branch", "unit", "project", "consortium", "alliance", "hub", "taskforce", "incubator", "accelerator"
]

# --- Categorization logic ---
def categorize_customer(name):
    if pd.isna(name) or not str(name).strip():
        return "Needs Review"

    name_lower = str(name).lower()
    word_count = len(name_lower.split())

    if any(re.search(rf'\\b{kw}\\b', name_lower) for kw in non_individual_keywords):
        return "Other"

    if word_count <= 3:
        return "Individual"

    return "Needs Review"

# --- Process file ---
if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        if 'Customer Name' not in df.columns:
            st.error("❌ 'Customer Name' column not found in the uploaded file.")
        else:
            df['Category'] = df['Customer Name'].apply(categorize_customer)
            st.success("✅ Categorization complete!")

            # Show preview
            st.subheader("Preview")
            st.dataframe(df.head(10))

            # Create downloadable Excel
            output = BytesIO()
            df.to_excel(output, index=False, engine='openpyxl')
            st.download_button(
                label="📥 Download Categorized Excel",
                data=output.getvalue(),
                file_name="categorized_customers.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    except Exception as e:
        st.error(f"Error: {e}")
