import tkinter as tk
from tkinter import filedialog, messagebox
import random
from collections import Counter
from finance_report import extract_spends_from_csv


class FoodDeciderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Food Decider App")
        self.root.geometry("400x250")

        # Initialize data containers
        self.food_spends = []
        self.places = []
        self.favorite_place = None

        # UI Elements
        load_btn = tk.Button(root, text="Load CSV Files", command=self.load_csvs)
        load_btn.pack(pady=10)

        suggest_btn = tk.Button(
            root, text="Suggest Random Place", command=self.suggest_place
        )
        suggest_btn.pack(pady=5)

        favorite_btn = tk.Button(
            root, text="Show Favorite Place", command=self.show_favorite
        )
        favorite_btn.pack(pady=5)

        # Button to list all visit counts
        list_btn = tk.Button(root, text="List All Visits", command=self.show_all_visits)
        list_btn.pack(pady=5)

        # Dropdown to select sort order
        self.sort_var = tk.StringVar(root)
        self.sort_var.set("Count")
        sort_frame = tk.Frame(root)
        sort_frame.pack(pady=(0, 5))
        tk.Label(sort_frame, text="Sort by:").pack(side=tk.LEFT)
        tk.OptionMenu(sort_frame, self.sort_var, "Count", "Name").pack(side=tk.LEFT)

        # Listbox for showing all visits
        visits_frame = tk.Frame(root)
        visits_frame.pack(fill=tk.BOTH, expand=True)
        self.listbox = tk.Listbox(visits_frame, width=50, height=10)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = tk.Scrollbar(
            visits_frame, orient=tk.VERTICAL, command=self.listbox.yview
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar.set)

        self.result_label = tk.Label(root, text="", wraplength=350, justify="center")
        self.result_label.pack(pady=20)

    def load_csvs(self):
        files = filedialog.askopenfilenames(
            title="Select CSV Files", filetypes=[("CSV Files", "*.csv")]
        )
        if not files:
            return
        # Load all spends and filter by CSV-provided 'Food' category
        spends = []
        for f in files:
            spends.extend(extract_spends_from_csv(f))
        # Only use entries where CSV category is explicitly 'Food'
        self.food_spends = [
            (date, desc, amount)
            for date, desc, amount, csv_cat in spends
            if csv_cat == "Food & Drink"
        ]
        if not self.food_spends:
            messagebox.showwarning(
                "No Food Data", "No food spending found in selected files."
            )
            return
        # Build visit counts and identify favorite place
        self.visit_counts = Counter(desc for date, desc, amount in self.food_spends)
        self.favorite_place = self.visit_counts.most_common(1)[0][0]
        # Build unique places list preserving original order
        self.places = list(
            dict.fromkeys(desc for date, desc, amount in self.food_spends)
        )
        messagebox.showinfo("Data Loaded", f"Loaded {len(self.places)} food entries.")

    def suggest_place(self):
        if not self.places:
            messagebox.showwarning("No Data", "Please load CSV files first.")
            return
        choice = random.choice(self.places)
        # Show suggestion in an alert box
        messagebox.showinfo("Suggestion", f"How about: {choice}?")
        # Also update the label
        self.result_label.config(text=f"How about: {choice}?")

    def show_favorite(self):
        if not self.favorite_place:
            messagebox.showwarning("No Data", "Please load CSV files first.")
            return
        # Show favorite place in an alert box
        messagebox.showinfo(
            "Favorite Place", f"Your favorite place is: {self.favorite_place}"
        )
        # Also update the label
        self.result_label.config(text=f"Your favorite place is: {self.favorite_place}")

    def show_all_visits(self):
        if not hasattr(self, "visit_counts") or not self.visit_counts:
            messagebox.showwarning("No Data", "Please load CSV files first.")
            return
        # Populate listbox with sorted visit counts
        self.listbox.delete(0, tk.END)
        sort_option = self.sort_var.get()
        if sort_option == "Count":
            items = sorted(self.visit_counts.items(), key=lambda x: x[1], reverse=True)
        else:  # Name
            items = sorted(self.visit_counts.items(), key=lambda x: x[0])
        for place, count in items:
            self.listbox.insert(tk.END, f"{place}: {count} visits")


if __name__ == "__main__":
    root = tk.Tk()
    app = FoodDeciderApp(root)
    root.mainloop()
