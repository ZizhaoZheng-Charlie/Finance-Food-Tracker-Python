import tkinter as tk
from tkinter import filedialog, messagebox
import os
from finance_report import save_report


class FinanceReportApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Finance Report Generator")
        self.root.geometry("400x250")
        self.csv_files = []

        self.label = tk.Label(
            root, text="Select CSV files to generate PDF report:", font=("Arial", 12)
        )
        self.label.pack(pady=10)

        self.select_button = tk.Button(
            root, text="Select CSVs", command=self.select_csvs
        )
        self.select_button.pack(pady=5)

        self.files_label = tk.Label(root, text="", wraplength=350, justify="left")
        self.files_label.pack(pady=5)

        self.generate_button = tk.Button(
            root,
            text="Generate PDF Report",
            command=self.generate_report,
            state=tk.DISABLED,
        )
        self.generate_button.pack(pady=20)

    def select_csvs(self):
        files = filedialog.askopenfilenames(
            title="Select CSV files", filetypes=[("CSV Files", "*.csv")]
        )
        if files:
            self.csv_files = list(files)
            self.files_label.config(text="\n".join(self.csv_files))
            self.generate_button.config(state=tk.NORMAL)
        else:
            self.files_label.config(text="")
            self.generate_button.config(state=tk.DISABLED)

    def generate_report(self):
        if not self.csv_files:
            messagebox.showwarning("No Files", "Please select CSV files first.")
            return
        try:
            save_report(self.csv_files)
            messagebox.showinfo(
                "Success",
                "Finance report (PDF) generated and saved to finance_reports folder.",
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {e}")


def main():
    root = tk.Tk()
    app = FinanceReportApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
