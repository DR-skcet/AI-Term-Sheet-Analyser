# parser/xlsx_parser.py
import pandas as pd

def parse_xlsx(file_path):
    df = pd.read_excel(file_path, engine='openpyxl')
    extracted = {}

    for field in ["Trade ID", "Date", "Party A", "Party B", "Instrument", "Amount", "Maturity Date"]:
        row = df[df.iloc[:, 0].astype(str).str.contains(field, case=False, na=False)]
        if not row.empty:
            extracted[field] = row.iloc[0, 1]
        else:
            extracted[field] = None

    return extracted
