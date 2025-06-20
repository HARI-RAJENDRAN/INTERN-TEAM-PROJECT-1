# ─────────────────────────────────────────────────────────────────────────────
#  Offer‑Letter PDF Generator – FINAL MAIN SCRIPT (with multi_cell fix)
# ─────────────────────────────────────────────────────────────────────────────
import os
import textwrap
import pandas as pd
from fpdf import FPDF

# ---------------------------------------------------------------------------
# CONSTANTS – adjust as needed
# ---------------------------------------------------------------------------
CSV_URL   = ("https://docs.google.com/spreadsheets/d/e/2PACX-1vTxaUq2leO_eZIQWMWzeSEtBbj0tknrnkhLInZjND3MfkRgZ77qBgWPVnDm6w-rEUFbt5pp5dBTyMLD/pub?output=csv")

TEMPLATE_PATH = "pdf_modi.txt"   # your offer‑letter template
OUTPUT_DIR    = r"C:\Users\Academytraining\Documents\generated_pds"

FONT_PATH     = r"C:\Users\Academytraining\Documents\VISUAL STUDIO\DejaVuSans.ttf"
FONT_FAMILY   = "DejaVu"         # internal name we give the font

LINE_HEIGHT   = 6                # 6 mm for 12 pt text
MARGIN_LEFT   = 20
MARGIN_RIGHT  = 20
WRAP_COLS     = 100              # characters before we wrap manually

# ---------------------------------------------------------------------------
# Helper: add two‑column row (label/value pairs)
# ---------------------------------------------------------------------------
def two_col(pdf, label1, value1, label2, value2, w=75, lh=LINE_HEIGHT):
    """
    Place two pieces of info side by side:
        label1: value1          label2: value2
    """
    pdf.cell(0, lh, "")               # reset to full‑width line start
    x_start = pdf.get_x()
    y_start = pdf.get_y()

    pdf.multi_cell(w, lh, f"{label1}: {value1}", border=0)
    pdf.set_xy(x_start + w + 5, y_start)  # 5‑mm gutter
    pdf.multi_cell(w, lh, f"{label2}: {value2}", border=0)
    pdf.ln(lh)

# ---------------------------------------------------------------------------
# 1)  Load data from Google Sheets
# ---------------------------------------------------------------------------
print("📥  Reading Google Sheet …")
df = pd.read_csv(CSV_URL)
df.columns = df.columns.str.strip()   # clean any stray spaces

# ---------------------------------------------------------------------------
# 2)  Ensure output directory exists
# ---------------------------------------------------------------------------
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# 3)  Loop through rows → create PDFs
# ---------------------------------------------------------------------------
for _, row in df.iterrows():
    # ‑‑‑ Build a dict for simpler formatting ‑‑‑
    user = {
        "Name"        : row.get("Name", ""),
        "Domain"      : row.get("Domain", ""),
        "Age"         : row.get("Age", ""),
        "Email"       : row.get("Email", ""),
        "CollegeName" : row.get("College Name", ""),
        "PhoneNumber" : row.get("Phone Number/Whatsapp Number", ""),
        "Year"        : row.get("Year", ""),
        "Gender"      : row.get("Gender Male/Female", ""),
        "Technology"  : row.get("Technology", ""),
        "StartDate"   : row.get("Start Date", ""),
        "EndDate"     : row.get("End Date", ""),
        "Stipend"     : row.get("Stipend", "")
    }

    # ‑‑‑ Load and substitute template placeholders ‑‑‑
    if not os.path.isfile(TEMPLATE_PATH):
        print("❌  Template file not found:", TEMPLATE_PATH)
        break

    with open(TEMPLATE_PATH, encoding="utf-8") as f:
        content = f.read()
        for key, value in user.items():
            content = content.replace(f"{{{{{key}}}}}", str(value))

    # ‑‑‑ Build PDF ‑‑‑
    pdf = FPDF(format="A4")
    pdf.set_left_margin(MARGIN_LEFT)
    pdf.set_right_margin(MARGIN_RIGHT)
    pdf.add_page()

    # Set page width for safe wrapping
    page_width = pdf.w - pdf.l_margin - pdf.r_margin

    # Try to add DejaVu font (Unicode); fall back to core Arial if missing
    if os.path.isfile(FONT_PATH):
        pdf.add_font(FONT_FAMILY, "", FONT_PATH)
        pdf.set_font(FONT_FAMILY, size=12)
    else:
        print("⚠️  Font file not found — using core Arial (limited Unicode).")
        pdf.set_font("Arial", size=12)

    # Write body with wrapping (fixing FPDFException crash)
    for paragraph in content.split("\n"):
        if paragraph.strip():
            for line in textwrap.wrap(paragraph, width=WRAP_COLS, break_long_words=True):
                pdf.multi_cell(page_width, LINE_HEIGHT, line)
        pdf.ln(LINE_HEIGHT)

    # ‑‑‑ Save file ‑‑‑
    safe_name = user["Name"].strip().replace(" ", "_").replace("/", "_")
    filename  = f"OfferLetter_{safe_name}.pdf"
    filepath  = os.path.join(OUTPUT_DIR, filename)
    pdf.output(filepath)
    print(f"✅  Generated {filename}")

print("🎉  All PDFs generated successfully!")
