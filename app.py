import streamlit as st
import pandas as pd
import re

# EXTENSIVE list of global non-individual keywords (cleaned, lowercase)
non_individual_keywords = [
    "inc", "inc.", "llc", "l.l.c.", "ltd", "ltd.", "limited", "corp", "corporation", "co", "co.",
    "pte", "pvt", "llp", "gmbh", "ag", "nv", "bv", "kk", "oy", "ab", "plc", "s.a", "s.a.s", "sa", "sarl",
    "sl", "aps", "as", "kft", "pt", "sdn", "bhd", "university", "uni", "institute", "inst", "college",
    "academy", "school", "faculty", "dept", "department", "cnrs", "research", "laboratory", "lab",
    "education", "educational", "engineering", "polytechnic", "polytech", "state", "centre", "center",
    "r&d", "science", "sciences", "technical", "technological", "technology", "innovation", "biotech",
    "medtech", "ai", "ml", "cybernetics", "govt", "government", "ngo", "n.g.o", "nonprofit",
    "non-profit", "ministry", "embassy", "consulate", "office", "admin", "administration",
    "secretariat", "authority", "commission", "agency", "bureau", "solutions", "consulting",
    "consultants", "advisory", "advisors", "partners", "partnership", "associates", "services",
    "ventures", "enterprises", "management", "finance", "capital", "holdings", "intl",
    "international", "global", "industries", "logistics", "trading", "procurement", "group",
    "store", "shop", "bookshop", "library", "distribution", "distributors", "outlet", "media",
    "publications", "books", "press", "foundation", "fondation", "fondazione", "trust", "union",
    "syndicate", "board", "chamber", "association", "club", "society", "network", "cooperative",
    "federation", "council", "committee", "coalition", "initiative", "team", "division", "branch",
    "unit", "project", "consortium", "alliance", "hub", "taskforce", "incubator", "accelerator",
    "pharmacy", "tech", "univ","state"
]

non_individual_keywords = list(set(non_individual_keywords))  # Remove duplicates

# Helper: Check if any keyword appears in the customer name
def contains_keyword(name):
    name_lower = name.lower()
    return any(kw in name_lower for kw in non_individual_keywords)

# Categorize customer name
def categorize_name(name):
    if not name or pd.isna(name) or name.strip() == "":
        return "Out of Scope"

    words = name.strip().split()

    if contains_keyword(name):
        return "Out of Scope"

    if len(words) == 1:
        return "For Review"

    # Handle Dr. John Clinic, Ms Smith Hospital etc.
    name_lower = name.lower()
    if re.search(r"(dr\.?|mr\.?|ms\.?|mrs\.?|prof\.?)(\s+[a-z]+){1,2}$", name_lower):
        return "In Scope"

    if 1 < len(words) <= 3:
        return "In Scope"

    return "Out of Scope"

# Streamlit App
st.set_page_config(page_title="Customer Categorization", layout="wide")
st.title("🔍 Customer Classification: In Scope vs Out of Scope")

uploaded_file = st.file_uploader("📤 Upload Excel File", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    if "Customer Name" not in df.columns:
        st.error("'Customer Name' column is missing from the uploaded file.")
    else:
        df["Category"] = df["Customer Name"].apply(categorize_name)

        st.success("✅ Classification Complete")
        st.dataframe(df.head(50), use_container_width=True)

        output = df.to_excel(index=False, engine="openpyxl")
        st.download_button(
            label="📥 Download Categorized Excel",
            data=output,
            file_name="categorized_customers.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        st.markdown("---")
        st.markdown("🔄 **Accuracy Tips**: This tool is based on advanced keyword detection. For enhanced enrichment (online lookup), ask to enable advanced API integration in the next version.")
else:
    st.info("👈 Please upload an Excel file with a 'Customer Name' column.")
