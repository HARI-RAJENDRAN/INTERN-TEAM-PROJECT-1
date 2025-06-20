import os
import pandas as pd
from fpdf import FPDF
import textwrap

# Downloaded font path (DejaVuSans.ttf should be in the same folder)
FONT_PATH = r"C:\Users\Academytraining\Documents\VISUAL STUDIO\DejaVuSans.ttf"



# Your published CSV link from Google Sheets
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTxaUq2leO_eZIQWMWzeSEtBbj0tknrnkhLInZjND3MfkRgZ77qBgWPVnDm6w-rEUFbt5pp5dBTyMLD/pub?output=csv"

# Ensure output folder exists
output_folder = r"C:\Users\Academytraining\Documents\generated_pds"
os.makedirs(output_folder, exist_ok=True)

# Read the sheet
df = pd.read_csv(sheet_url)
df.columns = df.columns.str.strip()  # Strip whitespace from column names

# PDF layout settings
LINE_HEIGHT = 6
MARGIN_LEFT = 20
MARGIN_RIGHT = 20

# Helper function to add two-column rows
def two_col(pdf, label1, value1, label2, value2, w=75, lh=6):
    pdf.cell(0, lh, "")  # reset line
    x = pdf.get_x()
    y = pdf.get_y()

    pdf.multi_cell(w, lh, f"{label1}: {value1}", border=0)
    pdf.set_xy(x + w + 5, y)
    pdf.multi_cell(w, lh, f"{label2}: {value2}", border=0)
    pdf.ln(lh)

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
        print("❌ Error: pdf_modi.txt template not found!")
        continue

    # Create a new PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_left_margin(MARGIN_LEFT)
    pdf.set_right_margin(MARGIN_RIGHT)

    # Add Unicode font
    pdf.add_font("DejaVu", "", FONT_PATH, uni=True)
    pdf.set_font("DejaVu", size=12)

    # Write the content
    for paragraph in content.split("\n"):
        if paragraph.strip():
            # Wrap long lines
            for line in textwrap.wrap(paragraph, width=100):
                pdf.multi_cell(0, LINE_HEIGHT, line)
        pdf.ln(LINE_HEIGHT)

    # Save the PDF
    filename = f"OfferLetter_{user_data['Name'].strip().replace(' ', '_').replace('/', '_')}.pdf"
    filepath = os.path.join(output_folder, filename)
    pdf.output(filepath)
    print(f"✅ PDF generated for: {user_data['Name']} at {filepath}")
