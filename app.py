import streamlit as st
import pandas as pd
import os
from io import BytesIO
from names_dataset import NameDataset

# Load name database
@st.cache_resource
def load_name_dataset():
    return NameDataset()
nd = load_name_dataset()

# Company-related keywords (extensive)
company_keywords = [
    "inc", "ltd", "llc", "plc", "corp", "co.", "company", "corporation", "incorporated",
    "gmbh", "s.a.", "s.a", "sa", "pte", "pty", "bv", "kg", "kgaa", "oy", "ab", "srl", "sro",
    "foundation", "trust", "association", "group", "partners", "industries", "enterprise",
    "consulting", "ventures", "technologies", "systems", "solutions", "services", "university",
    "college", "institute", "school", "bank", "society", "ngo", "cooperative", "govt", "government",
    "ministries", "municipal", "hospital", "clinic", "holding", "limited", "union", "agency", "club"
]

# Check name category
def classify_name(name):
    try:
        name = str(name).strip()
        name_lower = name.lower()

        # Check for company keywords
        for keyword in company_keywords:
            if keyword in name_lower:
                return "Out of Scope"

        # Check if it's a known first name
        first_word = name.split()[0]
        result = nd.search(first_word)
        if result and 'first_name' in result:
            return "In Scope"
    except:
        pass
    return "Out of Scope"

# UI starts here
st.set_page_config(page_title="Customer Categorization AI", layout="centered")
st.title("🧠 Ultra Accurate Customer Name Categorization")
st.markdown("This tool uses AI + Global Company Keywords to classify customers as **In Scope (Individuals)** or **Out of Scope (Companies)**.")

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
