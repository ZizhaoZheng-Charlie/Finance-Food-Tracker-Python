# Finance Analytics Suite

A Python-based personal finance analysis suite that helps you track, categorize, and analyze your spending habits.

## Features

### Finance Report Generator

- Automatically categorizes your banking transactions into categories (Food, Travel, Utilities, Shopping, etc.)
- Processes CSV files from your bank statements
- Generates detailed PDF reports of your spending by category
- GUI interface for easy CSV selection and report generation

### Food Decider App

- Analyzes your dining expenditures from bank statements
- Suggests random places to eat based on your past history
- Shows your most frequently visited food places
- Lists all your dining visits with sorting options (by count or name)

## Requirements

- Python 3.6+
- Required Python packages:
  - tkinter
  - reportlab
  - google-generativeai (for AI-based transaction categorization)

## Installation

1. Clone this repository
2. Create a virtual environment (recommended)
   ```
   python -m venv myenv
   myenv\Scripts\activate  # Windows
   source myenv/bin/activate  # Linux/Mac
   ```
3. Install required packages
   ```
   pip install reportlab google-generativeai
   ```

## Usage

### Finance Report Generator

```
python finance_report_gui.py
```

1. Click "Select CSVs" to choose your bank statement CSV files
2. Click "Generate PDF Report" to create a categorized spending report

### Food Decider App

```
python food_decider_app.py
```

1. Click "Load CSV Files" to choose your bank statement CSV files
2. Use the provided buttons to:
   - Get a random restaurant suggestion
   - See your favorite (most visited) place
   - View a list of all your dining visits

## CSV File Format

The application supports bank statement CSV files with the following column formats:

1. `Posting Date`, `Description`, `Amount`
2. `Post Date`, `Description`, `Amount`

Transactions with "Food & Drink" in the Category column will be used by the Food Decider App.

## Output

Generated PDF reports will be saved in a `finance_reports` folder in the same directory as the application.
