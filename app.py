import streamlit as st
import os
import json
from parser.pdf_parser import parse_pdf
from parser.docx_parser import parse_docx
from parser.xlsx_parser import parse_xlsx
from validator.rule_engine import validate_term_sheet, convert_dates

st.set_page_config(page_title="📄 AI Term Sheet Validator", layout="centered")
st.title("📄 AI-Powered Term Sheet Analyzer")

st.markdown("""
Upload a **term sheet** (`.pdf`, `.docx`, `.xlsx`) to automatically:
- 🧠 Extract structured data
- ✅ Validate trade, party, amount & date fields
- 💾 Download verified output as JSON
""")

uploaded_file = st.file_uploader("📤 Upload Your Term Sheet", type=["pdf", "docx", "xlsx"])

if uploaded_file:
    # Save to disk
    file_path = os.path.join("data", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"✅ Uploaded `{uploaded_file.name}`")

    # Detect file type and parse
    with st.spinner("🔍 Extracting data from document..."):
        if uploaded_file.name.endswith(".pdf"):
            extracted_data = parse_pdf(file_path)
            file_icon = "📄 PDF File"
        elif uploaded_file.name.endswith(".docx"):
            extracted_data = parse_docx(file_path)
            file_icon = "📝 Word Document"
        elif uploaded_file.name.endswith(".xlsx"):
            extracted_data = parse_xlsx(file_path)
            file_icon = "📊 Excel Spreadsheet"
        else:
            st.error("❌ Unsupported file type.")
            st.stop()

    st.info(f"File Type Detected: **{file_icon}**")

    with st.expander("🔍 Extracted Data (Click to View)"):
        st.json(extracted_data)

    # Validate
    result = validate_term_sheet(extracted_data)

    st.subheader("✅ Validation Result")
    if result["status"] == "Valid":
        st.success("✅ **Status: Valid** — No validation errors found.")
    else:
        st.error("❌ **Status: Invalid**")
        with st.expander("⚠️ View Issues"):
            for err in result["errors"]:
                st.markdown(f"- {err}")

    # Save validated data — convert datetime to string first
    output_path = os.path.join("output", uploaded_file.name + ".json")
    with open(output_path, "w") as f:
        json.dump(convert_dates(result), f, indent=2)

    st.download_button(
        label="📥 Download Validated Output (JSON)",
        data=json.dumps(convert_dates(result), indent=2),
        file_name="validated_output.json",
        mime="application/json"
    )

    st.markdown("---")
    st.caption("🛠️ Built with Streamlit,Python,GroqCloud,Llama-3")
