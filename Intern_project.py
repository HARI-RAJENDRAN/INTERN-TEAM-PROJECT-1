import os
import pandas as pd
from fpdf import FPDF

# ✅ Your published CSV link from Google Sheets
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTxaUq2leO_eZIQWMWzeSEtBbj0tknrnkhLInZjND3MfkRgZ77qBgWPVnDm6w-rEUFbt5pp5dBTyMLD/pub?output=csv"

# ✅ Read the sheet
df = pd.read_csv(sheet_url)
df.columns = df.columns.str.strip()

# ✅ Create output folder if it doesn't exist
output_folder = "generated_pdfs"
os.makedirs(output_folder, exist_ok=True)

# ✅ Loop through each row to generate PDFs
for index, row in df.iterrows():
    user_data = {
        "Name": row["Name"],
        "Domain": row["Domain"],
        "Age": ""  # Optional
    }

    # ✅ Load and fill the offer letter template
    with open("pdf_modi.txt", "r", encoding="utf-8") as f:
        content = f.read()
        for key, value in user_data.items():
            content = content.replace(f"{{{{{key}}}}}", str(value))

    # ✅ Generate the PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in content.split('\n'):
        pdf.cell(200, 10, txt=line, ln=True)

    # ✅ Save the PDF in the specific folder
    filename = f"OfferLetter_{user_data['Name'].strip().replace(' ', '_')}.pdf"
    filepath = os.path.join(output_folder, filename)
    pdf.output(filepath)

    print(f"✅ PDF generated for: {user_data['Name']} at {filepath}")
