import os
import pandas as pd
from flask import Flask, request, render_template, send_file
from names_dataset import NameDataset

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['PROCESSED_FOLDER'] = 'processed'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)

# Initialize name-dataset once
nd = NameDataset()

# Out of Scope Keywords
out_of_scope_keywords = [
    'ltd', 'inc', 'corp', 'university', 'company', 'foundation', 'trust', 'société', 'sarl',
    'gmbh', 'llp', 'plc', 'cooperative', 'bank', 'college', 'group', 'enterprise', 'firm',
    'bv', 'srl', 'sas', 'holding', 'limited', 'association', 'industries', 'partners'
]

def categorize_name(name):
    if not isinstance(name, str):
        return 'Out of Scope'
    
    name_lower = name.lower()
    if 'needs review' in name_lower:
        return 'Out of Scope'
    
    if any(kw in name_lower for kw in out_of_scope_keywords):
        return 'Out of Scope'
    
    tokens = name.split()
    for token in tokens:
        res = nd.search(token)
        if res['first_name'] or res['last_name']:
            return 'In Scope'
    
    return 'Out of Scope'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if not uploaded_file:
            return "No file uploaded"

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        uploaded_file.save(file_path)

        if uploaded_file.filename.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)

        name_col = df.columns[0]  # Assume name is in the first column
        df['Category'] = df[name_col].apply(categorize_name)

        output_path = os.path.join(app.config['PROCESSED_FOLDER'], 'categorized_output.xlsx')
        df.to_excel(output_path, index=False)

        return send_file(output_path, as_attachment=True)

    return render_template('index.html')
