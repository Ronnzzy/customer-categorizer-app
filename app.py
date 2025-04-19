import streamlit as st
import pandas as pd
import re
from io import BytesIO
import os

# === GLOBAL CONFIG ===
st.set_page_config(page_title="Customer Categorizer", layout="wide")
st.title("🌍 Global Customer Categorizer")

# === LOAD GLOBAL FIRST NAMES ===
@st.cache_data
def load_first_names():
    global_names_df = pd.read_csv("first_names_global.csv")
    return set(global_names_df['first_name'].str.lower().dropna())

global_first_names = load_first_names()

# === GLOBAL NON-INDIVIDUAL KEYWORDS ===
non_individual_keywords = [
    "inc", "ltd", "llc", "gmbh", "sarl", "plc", "pvt", "company", "co.", "corp", "university", "trust",
    "foundation", "group", "ngo", "club", "committee", "society", "industries", "dealers", "hospital",
    "clinic", "lab", "government", "ministry", "municipal", "board", "authority", "council", "academy",
    "enterprise", "consultancy", "solutions", "trading", "school", "association", "firm", "services",
    "export", "import", "technologies", "logistics", "estates", "realty", "stores", "foundation",
    "center", "centre", "team", "partners", "bureau", "office", "holding", "federal", "bank", "college",
    "retail", "distributors", "cooperative", "syndicate", "church", "mosque", "temple", "studio",
    "salon", "mart", "hub", "garage", "pharmacy", "medical", "labs", "station", "market", "network",
    "telecom", "fleet", "bazar", "outlet", "media", "radio", "tv", "channel", "institute"
]

# === STRIP KNOWN TITLES ===
titles_regex = r"\b(mr|mrs|ms|miss|dr|shri|smt|sir|madam|prof|hon|rev|capt|fr)\.?\b"

# === CATEGORIZATION FUNCTION ===
def categorize_customer(name: str) -> str:
    if not isinstance(name, str) or name.strip() == "":
        return "Out of Scope"

    name_clean = re.sub(titles_regex, "", name.strip().lower()).strip()

    # Check keywords for Out of Scope
    if any(keyword in name_clean for keyword in non_individual_keywords):
        return "Out of Scope"

    # Tokenize by space/hyphen
    words = re.split(r"[\s\-]+", name_clean)

    if len(words) == 1:
        return "For Review" if words[0] not in global_first_names else "In Scope"

    # Check if any part matches known global names
    matches = [word for word in words if word in global_first_names]
    return "In Scope" if matches else "Out of Scope"

# === FILE UPLOAD ===
uploaded_file = st.file_uploader("📁 Upload your Excel file (.xlsx or .xlsb)", type=["xlsx", "xlsb"])

if uploaded_file:
    # Determine file format
    file_ext = os.path.splitext(uploaded_file.name)[-1]

    # Read the file
    if file_ext == ".xlsx":
        df = pd.read_excel(uploaded_file)
    elif file_ext == ".xlsb":
        import pyxlsb
        df = pd.read_excel(uploaded_file, engine="pyxlsb")
    else:
        st.error("Unsupported file format.")
        st.stop()

    # Show preview
    st.subheader("Preview of Uploaded Data")
    st.dataframe(df.head(10))

    # Select the customer name column
    customer_column = st.selectbox("Select the Customer Name column", df.columns)

    # Apply categorization
    df["Scope Status"] = df[customer_column].apply(categorize_customer)

    # Display output
    st.subheader("🔍 Categorized Output")
    st.dataframe(df[[customer_column, "Scope Status"]])

    # Download output
    output = BytesIO()
    df.to_excel(output, index=False, engine="openpyxl")
    st.download_button("📥 Download Categorized File", data=output.getvalue(),
                       file_name="categorized_customers.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
