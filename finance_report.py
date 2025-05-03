import os
import json
import csv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from collections import defaultdict
import google.generativeai as genai


# Define common spend categories and keywords
CATEGORIES = {
    "Food": ["grocery", "restaurant", "cafe", "food", "supermarket"],
    "Travel": ["uber", "taxi", "flight", "hotel", "airbnb", "train", "bus"],
    "Utilities": ["electric", "water", "gas", "internet", "utility"],
    "Shopping": ["store", "mall", "shop", "amazon", "purchase"],
    "Other": [],
}

genai.configure(api_key=API_KEY)

# Load merchant-to-category mapping
MERCHANT_MAP_FILE = "merchant_categories.json"
if not os.path.exists(MERCHANT_MAP_FILE):
    with open(MERCHANT_MAP_FILE, "w", encoding="utf-8") as mf:
        json.dump({}, mf)
with open(MERCHANT_MAP_FILE, "r", encoding="utf-8") as mf:
    MERCHANT_MAP = json.load(mf)


# The expected CSV columns can be either:
# 1. Details, Posting Date, Description, Amount, Type, Balance, Check or Slip #
#    (use 'Posting Date' as date, 'Description' as description, 'Amount' as amount)
# 2. Transaction Date, Post Date, Description, Category, Type, Amount, Memo
#    (use 'Post Date' as date, 'Description' as description, 'Amount' as amount)
def extract_spends_from_csv(csv_path):
    """
    Extracts spend data from a CSV file with supported columns.
    Excludes rows where the description contains 'auto' or 'automatic' (case-insensitive).
    Returns a list of (date, description, amount, category) tuples.
    """
    spends = []
    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                # Try both possible formats
                if "Posting Date" in row and "Description" in row and "Amount" in row:
                    date = row["Posting Date"]
                    desc = row["Description"]
                    amount = float(row["Amount"])
                elif "Post Date" in row and "Description" in row and "Amount" in row:
                    date = row["Post Date"]
                    desc = row["Description"]
                    amount = float(row["Amount"])
                else:
                    continue
                # Exclude automate payments
                if "auto" in desc.lower() or "automatic" in desc.lower():
                    continue
                # Use CSV 'Category' column if available
                csv_cat = row.get("Category", "").strip() or None
                # Append date, description, amount, and optional CSV category
                spends.append((date, desc, amount, csv_cat))
            except (KeyError, ValueError):
                continue
    return spends


def gemini_categorize(description):
    prompt = (
        "You are a finance assistant. Categorize the following transaction description "
        "into one of these categories: Food, Travel, Utilities, Shopping, Other. "
        "Just return the category name. Description: '{}'"
    ).format(description)
    response = genai.chat(prompt)
    return response.text.strip()


def categorize_spend(description):
    desc_lower = description.lower()
    # 1. Check merchant-to-category mapping
    for merchant, cat in MERCHANT_MAP.items():
        if merchant.lower() in desc_lower:
            return cat
    # 2. Try AI-based categorization
    try:
        category = gemini_categorize(description)
        if category in CATEGORIES:
            return category
    except Exception:
        pass
    # Fallback to local keyword-based categorization
    for category, keywords in CATEGORIES.items():
        if any(keyword in desc_lower for keyword in keywords):
            return category
    return "Other"


def process_csvs(csv_paths):
    """
    Processes multiple CSVs and returns categorized spend data.
    Uses CSV-provided category when present, else AI/keyword logic.
    """
    categorized = defaultdict(list)
    for csv_path in csv_paths:
        entries = extract_spends_from_csv(csv_path)
        for date, desc, amount, csv_cat in entries:
            # Prefer CSV category if given
            if csv_cat:
                category = csv_cat
            else:
                category = categorize_spend(desc)
            categorized[category].append((date, desc, amount))
    return categorized


def generate_report_pdf(categorized_spends, output_path):
    """
    Generates a PDF report from categorized spends and saves it to output_path.
    """
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    y = height - 40
    c.setFont("Helvetica-Bold", 16)
    c.drawString(40, y, "Finance Report")
    y -= 30
    c.setFont("Helvetica", 12)
    total = 0
    for category, spends in categorized_spends.items():
        c.drawString(40, y, f"Category: {category}")
        y -= 20
        cat_total = 0
        for date, desc, amount in spends:
            c.drawString(60, y, f"{date} | {desc} | ${amount:.2f}")
            y -= 15
            cat_total += amount
            if y < 60:
                c.showPage()
                y = height - 40
        c.drawString(60, y, f"Total for {category}: ${cat_total:.2f}")
        y -= 25
        total += cat_total
        if y < 60:
            c.showPage()
            y = height - 40
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, y, f"Grand Total: ${total:.2f}")
    c.save()


def save_report(csv_paths, report_folder="finance_reports"):
    """
    Main function to process CSVs, generate, and save the PDF report.
    """
    if not os.path.exists(report_folder):
        os.makedirs(report_folder)
    categorized = process_csvs(csv_paths)
    report_path = os.path.join(report_folder, "finance_report.pdf")
    generate_report_pdf(categorized, report_path)
    print(f"Report saved to {report_path}")


if __name__ == "__main__":
    # Example usage:
    csv_files = ["statement1.csv", "statement2.csv"]
    save_report(csv_files)
