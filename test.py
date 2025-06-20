import os
import pandas as pd
from fpdf import FPDF

# Your published CSV link from Google Sheets
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTxaUq2leO_eZIQWMWzeSEtBbj0tknrnkhLInZjND3MfkRgZ77qBgWPVnDm6w-rEUFbt5pp5dBTyMLD/pub?output=csv"

# Read the sheet
df = pd.read_csv(sheet_url)
df.columns = df.columns.str.strip()  # Strip whitespace from column names

# Ensure output folder exists
output_folder = r"C:\Users\Academytraining\Documents\generated_pds"
os.makedirs(output_folder, exist_ok=True)

# Add a Unicode font once (make sure 'DejaVuSans.ttf' is in your script folder)
base_pdf = FPDF()
base_pdf.add_font('DejaVu', '', 'DejaVuSans.ttf')

# Loop through each row to generate PDFs
for index, row in df.iterrows():
    user_data = {
        "Name": row.get("Name", ""),
        "Domain": row.get("Domain", ""),
        "Age": row.get("Age", ""),
        "Email": row.get("Email", ""),
        "CollegeName": row.get("College Name", ""),
        "PhoneNumber": row.get("Phone Number/Whatsapp Number", ""),
        "Year": row.get("Year", ""),
        "Gender": row.get("Gender Male/Female", ""),
        "Technology": row.get("Technology", ""),
        "StartDate": row.get("Start Date", ""),
        "EndDate": row.get("End Date", ""),
        "Stipend": row.get("Stipend", "")
    }

    # Load and fill the offer letter template
    try:
        with open("pdf_modi.txt", "r", encoding="utf-8") as f:
            content = f.read()
            for key, value in user_data.items():
                content = content.replace(f"{{{{{key}}}}}", str(value))
    except FileNotFoundError:
        print("Error: pdf_modi.txt template not found!")
        continue

    # Create a new PDF for each user
    pdf = FPDF()
    pdf.add_font('DejaVu', '', 'DejaVuSans.ttf')
    pdf.add_page()
    pdf.set_font("DejaVu", size=12)

    pdf.multi_cell(0, 10, txt=content)

    filename = f"OfferLetter_{user_data['Name'].strip().replace(' ', '_').replace('/', '_')}.pdf"
    filepath = os.path.join(output_folder, filename)

    pdf.output(filepath)
    print(f"✅ PDF generated for: {user_data['Name']} at {filepath}")
