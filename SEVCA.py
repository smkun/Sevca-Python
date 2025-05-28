import tkinter as tk
from tkinter import ttk, filedialog
from tkcalendar import DateEntry
from datetime import datetime
from fpdf import FPDF
from PIL import Image, ImageTk
import json


class ClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SEVCA Client Worksheet")

        # === Show SEVCA Logo at the top ===
        logo_frame = ttk.Frame(root)
        logo_frame.pack(pady=(10, 0))
        

        try:
            image = Image.open("SEVCA-logo.jpg")
            image = image.resize((180, 80), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(image)
            self.logo_label = ttk.Label(logo_frame, image=photo)
            self.logo_label.image = photo  # keep reference to avoid garbage collection
            self.logo_label.pack()
        except Exception as e:
            print(f"⚠️ Could not load SEVCA-logo.jpg — {e}")

        # === Proceed with normal setup ===
        self.headers = [
            "Date", "Client Name", "Intake", "BP", "Story", "Finances",
            "MKT", "Ongoing Support", "FinCo", "Referred By", "Referred To"
        ]

        self.rows = []
        self.table_frame = ttk.Frame(root)
        self.table_frame.pack(padx=10, pady=10)

        self.build_table_headers()
        self.add_row()

        btn_frame = ttk.Frame(root)
        btn_frame.pack(pady=5)

        ttk.Button(btn_frame, text="Add Row", command=self.add_row).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Save JSON", command=self.save_json).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Load JSON", command=self.load_json).grid(row=0, column=2, padx=5)
        ttk.Button(btn_frame, text="Export PDF", command=self.export_pdf).grid(row=0, column=3, padx=5)

        footer = ttk.Label(root, text="© 2025 Scott Kunian – SEVCA Client Worksheet", font=("Arial", 8))
        footer.pack(pady=(5, 10))

    def build_table_headers(self):
        for col, header in enumerate(self.headers):
            lbl = ttk.Label(self.table_frame, text=header, font=('Arial', 10, 'bold'))
            lbl.grid(row=0, column=col, padx=3, pady=3)

    def add_row(self, data=None):
        r = []
        row_index = len(self.rows) + 1

        for col, header in enumerate(self.headers):
            if header == "Date":
                var = tk.StringVar(value=data.get(header, "") if data else "")
                ent = DateEntry(self.table_frame, textvariable=var, date_pattern='yyyy-mm-dd', width=12)
                ent.grid(row=row_index, column=col)
                r.append(var)
            elif header in ["Intake", "BP", "Story", "Finances", "MKT", "Ongoing Support"]:
                var = tk.BooleanVar(value=data.get(header, False) if data else False)
                chk = tk.Checkbutton(self.table_frame, variable=var)
                chk.grid(row=row_index, column=col)
                r.append(var)
            elif header == "FinCo":
                var = tk.StringVar(value=data.get(header, "") if data else "")
                opt = ttk.Combobox(self.table_frame, textvariable=var, values=["", "Yes", "No"], width=6)
                opt.grid(row=row_index, column=col)
                r.append(var)
            else:
                var = tk.StringVar(value=data.get(header, "") if data else "")
                ent = tk.Entry(self.table_frame, textvariable=var, width=15)
                ent.grid(row=row_index, column=col)
                r.append(var)

        self.rows.append(r)

    def save_json(self):
        data = []
        for r in self.rows:
            row = {
                self.headers[i]: (r[i].get() if not isinstance(r[i], tk.BooleanVar) else bool(r[i].get()))
                for i in range(len(r))
            }
            data.append(row)

        file_name = self.timestamped_filename("clients", "json")
        path = filedialog.asksaveasfilename(defaultextension=".json", initialfile=file_name)
        if path:
            with open(path, 'w') as f:
                json.dump(data, f, indent=2)

    def load_json(self):
        path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if not path:
            return
        with open(path) as f:
            data = json.load(f)

        for widget in self.table_frame.winfo_children():
            widget.destroy()
        self.rows = []
        self.build_table_headers()
        for entry in data:
            self.add_row(entry)

    def export_pdf(self):
        pdf = FPDF(orientation='L', unit='mm', format='A4')
        pdf.add_page()

        try:
            pdf.image("SEVCA-logo.jpg", x=10, y=8, w=30)
        except RuntimeError:
            print("⚠️ Could not load SEVCA-logo.jpg — skipping logo.")

        pdf.set_xy(45, 10)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "Client Worksheet", ln=True)

        col_widths = [22, 47, 14, 10, 17, 20, 14, 18, 17, 47, 47]

        def draw_headers():
            pdf.set_font("Arial", 'B', 9)
            pdf.set_fill_color(200, 200, 200)
            for i, header in enumerate(self.headers):
                pdf.cell(col_widths[i], 10, header, border=1, fill=True)
            pdf.ln()

        pdf.set_y(25)
        pdf.set_font("Arial", size=9)
        draw_headers()

        for r in self.rows:
            if pdf.get_y() > 185:
                pdf.add_page()
                draw_headers()
            for i, val in enumerate(r):
                content = val.get() if not isinstance(val, tk.BooleanVar) else ("Yes" if val.get() else "No")
                pdf.cell(col_widths[i], 8, str(content), border=1)
            pdf.ln()

        filename = self.timestamped_filename("client-worksheet", "pdf")
        pdf.output(filename)

    def timestamped_filename(self, prefix, extension):
        now = datetime.now()
        return f"{prefix}_{now.strftime('%Y-%m-%d_%H-%M-%S')}.{extension}"


if __name__ == "__main__":
    root = tk.Tk()
    app = ClientApp(root)
    root.mainloop()
"""
SEVCA Client Worksheet Form App
Created as a favor by Scott Kunian (c) 2025

This application allows data entry, JSON saving/loading, and PDF export
for SEVCA's client intake worksheet. Not for commercial use.
"""
