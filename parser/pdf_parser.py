# parser/pdf_parser.py
import pdfplumber
import re

def extract_text_from_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
    return text

def parse_pdf(file_path):
    text = extract_text_from_pdf(file_path)
    data = {
        "Trade ID": re.search(r"Trade ID:\s*(\S+)", text),
        "Date": re.search(r"Date:\s*([\d\-\/]+)", text),
        "Party A": re.search(r"Party A:\s*(.+)", text),
        "Party B": re.search(r"Party B:\s*(.+)", text),
        "Instrument": re.search(r"Instrument:\s*(\w+)", text),
        "Amount": re.search(r"Amount:\s*[\$USD ]*([\d,\.]+)", text),
        "Maturity Date": re.search(r"Maturity Date:\s*([\d\-\/]+)", text),
    }
    # Extract match group values
    return {k: v.group(1).strip() if v else None for k, v in data.items()}
