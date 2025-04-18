import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="Customer Categorization", layout="wide")
st.title("📋 Customer Categorization – In Scope / Out of Scope")

# Full keyword list for non-individuals
non_individual_keywords = [
    "inc", "inc.", "llc", "l.l.c.", "ltd", "ltd.", "limited", "corp", "corporation", "co", "co.", "pte", "pvt", "llp",
    "gmbh", "ag", "nv", "bv", "kk", "oy", "ab", "plc", "s.a", "s.a.s", "sa", "sarl", "sl", "aps", "as", "kft", "pt", "sdn", "bhd",
    "university", "uni", "institute", "inst", "college", "academy", "school", "faculty", "dept", "department", "cnrs",
    "research", "laboratory", "lab", "education", "educational", "engineering", "polytechnic", "polytech", "state",
    "centre", "center", "r&d", "science", "sciences", "technical", "technological", "technology", "innovation",
    "biotech", "medtech", "ai", "ml", "cybernetics", "govt", "government", "ngo", "n.g.o", "nonprofit", "non-profit",
    "ministry", "embassy", "consulate", "office", "admin", "administration", "secretariat", "authority", "commission",
    "agency", "bureau", "solutions", "consulting", "consultants", "advisory", "advisors", "partners", "partnership",
    "associates", "services", "ventures", "enterprises", "management", "finance", "capital", "holdings", "intl",
    "international", "global", "industries", "logistics", "trading", "procurement", "group", "store", "shop",
    "bookshop", "library", "distribution", "distributors", "outlet", "media", "publications", "books", "press",
    "foundation", "fondation", "fondazione", "trust", "union", "syndicate", "board", "chamber", "association",
    "club", "society", "network", "cooperative", "federation", "council", "committee", "coalition", "initiative",
    "team", "division", "branch", "unit", "project", "consortium", "alliance", "hub", "taskforce", "incubator", 
    "accelerator", "pharmacy", "tech", "univ"
]

# Convert list to regex pattern
non_individual_pattern = r"\b(" + "|".join(re.escape(k) for k in non_individual_keywords) + r")\b"

def categorize_customer(name):
    if not isinstance(name, str) or not name.strip():
        return "Needs Review"
    
    name_clean = name.strip().lower()
    
    if re.search(non_individual_pattern, name_clean):
        return "Out of Scope"
    
    word_count = len(name_clean.split())
    
    if 1 < word_count <= 3:
        return "In Scope"
    elif word_count == 1:
        return "Needs Review"
    else:
        return "Out of Scope"

# Upload section
uploaded_file = st.file_uploader("📤 Upload Excel File", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    
    if 'Customer Name' not in df.columns:
        st.error("❌ 'Customer Name' column not found in the file.")
    else:
        df['Category'] = df['Customer Name'].apply(categorize_customer)

        st.success("✅ Categorization Complete!")
        st.dataframe(df)

        # Download link
        output_file = "categorized_customers.xlsx"
        df.to_excel(output_file, index=False)

        with open(output_file, "rb") as f:
            st.download_button(
                label="📥 Download Categorized File",
                data=f,
                file_name="categorized_customers.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
