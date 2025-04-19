import streamlit as st
import pandas as pd
from io import BytesIO

# Set up the Streamlit app configuration
st.set_page_config(page_title="Customer Name Categorizer", layout="wide")
st.title("🌍 Worldwide Customer Name Categorizer")

# Keywords to identify non-individual entities
non_individual_keywords = [
    # Legal/Corporate Structures
    "inc", "llc", "corp", "corporation", "co", "co.", "pte", "pvt", "llp",
    "gmbh", "ag", "nv", "bv", "kk", "oy", "ab", "plc", "s.a", "s.a.s", "sa", 
    "sarl", "sl", "aps", "as", "kft", "pt", "sdn", "bhd",
    # Academic / Institutional
    "university", "uni", "institute", "inst", "college", "academy", "school", 
    "faculty", "dept", "department", "cnrs", "research", "laboratory", "lab", 
    "education", "educational", "engineering", "polytechnic", "polytech",
    # Science / R&D
    "centre", "center", "r&d", "science", "sciences", "technical", "technological", 
    "technology", "innovation", "biotech", "medtech", "ai", "ml", "cybernetics",
    # Government / NGO / Nonprofit
    "govt", "government", "ngo", "n.g.o", "nonprofit", "non-profit", "ministry", 
    "embassy", "consulate", "office", "admin", "administration", "secretariat", 
    "authority", "commission", "agency", "bureau",
    # Professional / Financial Services
    "solutions", "consulting", "consultants", "advisory", "advisors", "partners", 
    "partnership", "associates", "services", "ventures", "enterprises", "management", 
    "finance", "capital", "holdings", "intl", "international", "global", 
    "industries", "logistics", "trading", "procurement", "group",
    # Media / Publishing / Books / Retail
    "store", "shop", "bookshop", "library", "distribution", "distributors", 
    "outlet", "media", "publications", "books", "press",
    # Social / Community Organizations
    "foundation", "fondation", "trust", "union", "syndicate", "board", "chamber", 
    "association", "club", "society", "network", "cooperative", "federation", 
    "council", "committee", "coalition", "initiative",
    # Others (catch-all patterns)
    "team", "division", "branch", "unit", "project", "consortium", "alliance", 
    "hub", "taskforce", "incubator", "accelerator"
]

# Load worldwide names dataset (you can create this from existing databases)
@st.cache_data
def load_human_names():
    # Replace this with the actual path to your worldwide names dataset
    human_names_df = pd.read_csv("path/to/worldwide_names.csv")
    return set(human_names_df['name'].str.lower().dropna())  # Ensure 'name' is the correct column

# Load the human names set
global_human_names = load_human_names()

# Categorization function
def categorize_customer(name: str) -> str:
    if not isinstance(name, str) or name.strip() == "":
        return "Needs
