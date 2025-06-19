import pandas as pd
from fpdf import FPDF

# ✅ Your published CSV link from Google Sheets
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTxaUq2leO_eZIQWMWzeSEtBbj0tknrnkhLInZjND3MfkRgZ77qBgWPVnDm6w-rEUFbt5pp5dBTyMLD/pub?output=csv"

# ✅ Read the sheet, and clean column headersZ77qBgWPVnDm6w-rEUFbt5pp5dBTyMLD/pub?output=csv
df = pd.read_csv(sheet_url)
df.columns = df.columns.str.strip()  # Removes spaces like "Name "

# ✅ Loop through each row to generate PDFs
for index, row in df.iterrows():
    user_data = {
        "Name": row["Name"],
        "Domain": row["Domain"],
        "Age": ""  # Optional if Age isn't in the sheet
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

    # ✅ Save the PDF using the intern's name
    filename = f"OfferLetter_{user_data['Name'].strip().replace(' ', '_')}.pdf"
    pdf.output(filename)

    print(f"✅ PDF generated for: {user_data['Name']}")
