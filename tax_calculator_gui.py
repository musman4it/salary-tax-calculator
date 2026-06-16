import tkinter as tk
from tkinter import ttk, messagebox

TAX_SLABS = [
    (0, 600000, 0, 0, 0),
    (600001, 1200000, 0, 0.01, 600000),
    (1200001, 2200000, 6000, 0.11, 1200000),
    (2200001, 3200000, 116000, 0.23, 2200000),
    (3200001, 4100000, 346000, 0.30, 3200000),
    (4100001, float('inf'), 616000, 0.35, 4100000),
]

def calculate_tax(annual_income):
    for min_inc, max_inc, fixed_tax, pct, base in TAX_SLABS:
        if min_inc <= annual_income <= max_inc:
            base_tax = fixed_tax + ((annual_income - base) * pct)
            break
    surcharge = base_tax * 0.09 if annual_income > 10000000 else 0
    total_tax = base_tax + surcharge
    return total_tax, surcharge, annual_income - total_tax

class TaxCalculatorGUI:
    def __init__(self, root):
        self.root = root
        root.title("Pakistan Salary Tax Calculator - FBR 2025-26")
        root.configure(bg="#0f172a")
        root.resizable(False, False)

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TLabel", background="#0f172a", foreground="#f8fafc", font=("Segoe UI", 11))
        self.style.configure("TEntry", fieldbackground="#1e293b", foreground="#f8fafc", bordercolor="#334155")
        self.style.configure("TButton", background="#3b82f6", foreground="#ffffff", font=("Segoe UI", 10, "bold"), borderwidth=0)
        self.style.map("TButton", background=[("active", "#2563eb")])

        main_frame = tk.Frame(root, bg="#1e293b", padx=30, pady=25, highlightthickness=1, highlightbackground="#334155")
        main_frame.pack(padx=20, pady=20)

        tk.Label(main_frame, text="Pakistan Salary Tax Calculator", font=("Segoe UI", 20, "bold"), fg="#f8fafc", bg="#1e293b").pack(anchor="w")
        tk.Label(main_frame, text="FBR Progressive Tax Slabs 2025-26", font=("Segoe UI", 11), fg="#64748b", bg="#1e293b").pack(anchor="w", pady=(0, 18))

        input_frame = tk.Frame(main_frame, bg="#1e293b")
        input_frame.pack(fill="x")

        tk.Label(input_frame, text="Salary Amount (PKR)", font=("Segoe UI", 9, "bold"), fg="#94a3b8", bg="#1e293b").grid(row=0, column=0, sticky="w", pady=(0, 4))
        self.salary_var = tk.StringVar(value="80000")
        self.salary_entry = tk.Entry(input_frame, textvariable=self.salary_var, font=("Segoe UI", 14), bg="#0f172a", fg="#f8fafc", insertbackground="#f8fafc", relief="flat", bd=0, highlightthickness=1, highlightbackground="#334155", highlightcolor="#3b82f6", padx=12, pady=8, width=20)
        self.salary_entry.grid(row=1, column=0, padx=(0, 12), ipady=4)
        self.salary_entry.bind("<KeyRelease>", self.on_calculate)

        tk.Label(input_frame, text="Salary Mode", font=("Segoe UI", 9, "bold"), fg="#94a3b8", bg="#1e293b").grid(row=0, column=1, sticky="w", pady=(0, 4))
        self.mode_var = tk.StringVar(value="monthly")
        self.mode_combo = ttk.Combobox(input_frame, textvariable=self.mode_var, values=["monthly", "annual"], state="readonly", font=("Segoe UI", 12), width=12)
        self.mode_combo.grid(row=1, column=1, padx=(0, 12), ipady=4)
        self.mode_combo.bind("<<ComboboxSelected>>", self.on_calculate)

        self.calc_btn = tk.Button(input_frame, text="Calculate", command=self.on_calculate, font=("Segoe UI", 11, "bold"), bg="#3b82f6", fg="#ffffff", relief="flat", padx=24, pady=8, cursor="hand2", activebackground="#2563eb", activeforeground="#ffffff")
        self.calc_btn.grid(row=1, column=2)
        self.calc_btn.bind("<Enter>", lambda e: self.calc_btn.configure(bg="#2563eb"))
        self.calc_btn.bind("<Leave>", lambda e: self.calc_btn.configure(bg="#3b82f6"))

        sep = tk.Frame(main_frame, height=1, bg="#334155")
        sep.pack(fill="x", pady=18)

        self.results_frame = tk.Frame(main_frame, bg="#1e293b")
        self.results_frame.pack(fill="x")

        self.result_labels = {}
        result_items = [
            ("gross_annual", "Gross Annual Income", "blue"),
            ("gross_monthly", "Gross Monthly Income", "blue"),
            ("tax_annual", "Total Annual Tax", "red"),
            ("tax_monthly", "Total Monthly Tax", "red"),
            ("net_annual", "Net Annual Take-Home", "green"),
            ("net_monthly", "Net Monthly Take-Home", "green"),
        ]

        for i, (key, label, color) in enumerate(result_items):
            row, col = divmod(i, 2)
            card = tk.Frame(self.results_frame, bg="#0f172a", highlightthickness=1, highlightbackground="#334155", padx=14, pady=10)
            card.grid(row=row, column=col, padx=4, pady=4, sticky="ew")
            tk.Label(card, text=label, font=("Segoe UI", 9, "bold"), fg="#64748b", bg="#0f172a").pack(anchor="w")
            self.result_labels[key] = tk.Label(card, text="—", font=("Segoe UI", 16, "bold"), fg=color, bg="#0f172a")
            self.result_labels[key].pack(anchor="w", pady=(2, 0))
            self.results_frame.columnconfigure(col, weight=1)

        self.surcharge_label = tk.Label(main_frame, text="", font=("Segoe UI", 10), fg="#f59e0b", bg="#1e293b")
        self.surcharge_label.pack(anchor="w", pady=(6, 0))

        sep2 = tk.Frame(main_frame, height=1, bg="#334155")
        sep2.pack(fill="x", pady=14)

        tk.Label(main_frame, text="Slab-wise Tax Breakdown", font=("Segoe UI", 10, "bold"), fg="#94a3b8", bg="#1e293b").pack(anchor="w")

        self.slab_frame = tk.Frame(main_frame, bg="#1e293b")
        self.slab_frame.pack(fill="x", pady=(8, 0))

        self.on_calculate()

    def on_calculate(self, event=None):
        try:
            salary = float(self.salary_var.get())
        except ValueError:
            for v in self.result_labels.values():
                v.config(text="—")
            return

        mode = self.mode_var.get()
        annual = salary * 12 if mode == "monthly" else salary
        monthly = annual / 12

        total_tax, surcharge, net_annual = calculate_tax(annual)
        net_monthly = net_annual / 12

        def fmt(n):
            return f"PKR {n:,.2f}"

        self.result_labels["gross_annual"].config(text=fmt(annual))
        self.result_labels["gross_monthly"].config(text=fmt(monthly))
        self.result_labels["tax_annual"].config(text=fmt(total_tax))
        self.result_labels["tax_monthly"].config(text=fmt(total_tax / 12))
        self.result_labels["net_annual"].config(text=fmt(net_annual))
        self.result_labels["net_monthly"].config(text=fmt(net_monthly))

        self.surcharge_label.config(text="⚠ Includes 9% high-earner surcharge (income > 10M PKR)" if surcharge > 0 else "")

        for w in self.slab_frame.winfo_children():
            w.destroy()

        slab_data = [
            ("PKR 0 - 600,000", "0%"),
            ("PKR 600,001 - 1,200,000", "1%"),
            ("PKR 1,200,001 - 2,200,000", "11%"),
            ("PKR 2,200,001 - 3,200,000", "23%"),
            ("PKR 3,200,001 - 4,100,000", "30%"),
            ("PKR 4,100,001 & above", "35%"),
        ]

        remaining = annual
        cumulative_tax = 0
        slab_taxes = []

        for (min_inc, max_inc, fixed_tax, pct, base), (label, rate) in zip(TAX_SLABS, slab_data):
            max_show = max_inc if max_inc != float('inf') else annual
            if annual < min_inc:
                slab_taxes.append((label, rate, 0))
                continue
            taxable_in_slab = min(annual, max_inc) - max(0, min_inc - 1)
            tax_in_slab = max(0, (fixed_tax + (annual - base) * pct) - cumulative_tax)
            cumulative_tax = fixed_tax + (annual - base) * pct
            slab_taxes.append((label, rate, tax_in_slab))

        for label, rate, tax in slab_taxes:
            row = tk.Frame(self.slab_frame, bg="#0f172a" if slab_taxes.index((label, rate, tax)) % 2 == 0 else "#1e293b")
            row.pack(fill="x", pady=1)
            tk.Label(row, text=label, font=("Segoe UI", 10), fg="#94a3b8", bg=row["bg"]).pack(side="left", padx=8)
            tk.Label(row, text=rate, font=("Segoe UI", 10), fg="#64748b", bg=row["bg"]).pack(side="left", padx=8)
            tk.Label(row, text=fmt(tax), font=("Segoe UI", 10, "bold"), fg="#ef4444", bg=row["bg"]).pack(side="right", padx=8)


if __name__ == "__main__":
    root = tk.Tk()
    app = TaxCalculatorGUI(root)
    root.mainloop()
