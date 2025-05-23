# validator/rule_engine.py
from datetime import datetime

def is_valid_date(date_val):
    if isinstance(date_val, datetime):
        return date_val  # Already valid datetime object
    if isinstance(date_val, str):
        for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%Y/%m/%d"):
            try:
                return datetime.strptime(date_val, fmt)
            except ValueError:
                continue
    return None

def validate_term_sheet(data):
    errors = []
    
    # Check for missing fields
    for field in ["Trade ID", "Date", "Party A", "Party B", "Instrument", "Amount", "Maturity Date"]:
        if not data.get(field):
            errors.append(f"Missing value for '{field}'.")

    # Amount check
    try:
        amount = float(str(data.get("Amount", "")).replace(",", ""))
        if amount <= 0:
            errors.append("Amount must be greater than zero.")
    except:
        errors.append("Invalid amount format.")

    # Date comparison
    trade_date = is_valid_date(data.get("Date", ""))
    maturity_date = is_valid_date(data.get("Maturity Date", ""))
    if trade_date and maturity_date:
        if maturity_date <= trade_date:
            errors.append("Maturity Date must be after Trade Date.")
    else:
        errors.append("Invalid date format in Date or Maturity Date.")

    result = {
        "status": "Valid" if not errors else "Invalid",
        "errors": errors,
        "validated_data": data
    }

    return result

# Helper function to convert datetime objects to strings for JSON serialization
def convert_dates(obj):
    if isinstance(obj, dict):
        return {k: convert_dates(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_dates(i) for i in obj]
    elif isinstance(obj, datetime):
        return obj.strftime("%Y-%m-%d")
    else:
        return obj
