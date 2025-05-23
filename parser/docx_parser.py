# parser/docx_parser.py
from docx import Document
import re

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def parse_docx(file_path):
    text = extract_text_from_docx(file_path)
    data = {
        "Trade ID": re.search(r"Trade ID:\s*(\S+)", text),
        "Date": re.search(r"Date:\s*([\d\-\/]+)", text),
        "Party A": re.search(r"Party A:\s*(.+)", text),
        "Party B": re.search(r"Party B:\s*(.+)", text),
        "Instrument": re.search(r"Instrument:\s*(\w+)", text),
        "Amount": re.search(r"Amount:\s*[\$USD ]*([\d,\.]+)", text),
        "Maturity Date": re.search(r"Maturity Date:\s*([\d\-\/]+)", text),
    }
    return {k: v.group(1).strip() if v else None for k, v in data.items()}
