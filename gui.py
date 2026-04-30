import tkinter as tk
from tkinter import filedialog
from file_handler import load_data
from analyzer import SalesAnalyzer
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class App:
    def __init__(self, root):
        self.root = root
        self.df = None
        self.current_fig = None

        # ===== COLORS =====
        self.bg_dark = "#2c3e50"
        self.bg_light = "#ecf0f1"
        self.card_color = "#ffffff"

        # ===== LAYOUT =====
        self.sidebar = tk.Frame(root, width=220, bg=self.bg_dark)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        self.main_area = tk.Frame(root, bg=self.bg_light)
        self.main_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # ===== KPI SECTION =====
        self.kpi_frame = tk.Frame(self.main_area, bg=self.bg_light)
        self.kpi_frame.pack(fill=tk.X, pady=10)

        self.kpi_orders = self.create_kpi("🧾 Orders", "0")
        self.kpi_revenue = self.create_kpi("💰 Revenue", "0")
        self.kpi_products = self.create_kpi("📦 Products", "0")

        # ===== SCROLLABLE CHART AREA =====
        self.canvas_frame = tk.Canvas(self.main_area, bg=self.bg_light)
        self.scrollbar = tk.Scrollbar(self.main_area, orient="vertical", command=self.canvas_frame.yview)

        self.scrollable_frame = tk.Frame(self.canvas_frame, bg=self.bg_light)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas_frame.configure(scrollregion=self.canvas_frame.bbox("all"))
        )

        self.canvas_frame.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas_frame.configure(yscrollcommand=self.scrollbar.set)

        self.canvas_frame.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # ===== SIDEBAR =====
        tk.Label(self.sidebar, text="📊 Dashboard", bg=self.bg_dark, fg="white",
                 font=("Arial", 14, "bold")).pack(pady=10)

        tk.Button(self.sidebar, text="📂 Upload CSV", command=self.upload,
                  bg="#3498db", fg="white").pack(fill="x", pady=5)

        self.file_label = tk.Label(self.sidebar, text="No file", bg=self.bg_dark, fg="white")
        self.file_label.pack(pady=5)

        self.add_btn("📅 Orders by Date", self.show_orders)
        self.add_btn("📦 Top Products", self.show_products)
        self.add_btn("📍 Locations", self.show_locations)
        self.add_btn("💳 Payment", self.show_payment)
        self.add_btn("🏷 Discount", self.show_discount)
        self.add_btn("🏭 Vendors", self.show_vendor)

        tk.Button(self.sidebar, text="⬇ Export PNG", command=self.export_png,
                  bg="#27ae60", fg="white").pack(fill="x", pady=5)
        tk.Button(self.sidebar, text="⬇ Export PDF", command=self.export_pdf,
                  bg="#8e44ad", fg="white").pack(fill="x", pady=5)

    # ===== KPI CARD =====
    def create_kpi(self, title, value):
        frame = tk.Frame(self.kpi_frame, bg=self.card_color, bd=1, relief="solid")
        frame.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=10)

        label_title = tk.Label(frame, text=title, bg=self.card_color,
                               font=("Arial", 10))
        label_title.pack()

        label_value = tk.Label(frame, text=value, bg=self.card_color,
                               font=("Arial", 16, "bold"))
        label_value.pack()

        return label_value

    # ===== UPDATE KPI =====
    def update_kpis(self):
        if self.df is None:
            return

        df = self.df.copy()
        df.columns = df.columns.str.strip()

        total_orders = df['Name'].nunique() if 'Name' in df.columns else 0

        revenue = 0
        if 'Lineitem quantity' in df.columns and 'Lineitem price' in df.columns:
            revenue = (df['Lineitem quantity'] * df['Lineitem price']).sum()

        total_products = df['Lineitem name'].nunique() if 'Lineitem name' in df.columns else 0

        self.kpi_orders.config(text=str(total_orders))
        self.kpi_revenue.config(text=f"₹ {round(revenue, 2)}")
        self.kpi_products.config(text=str(total_products))

    def add_btn(self, text, cmd):
        tk.Button(self.sidebar, text=text, command=cmd,
                  bg="#34495e", fg="white").pack(fill="x", pady=2)

    # ===== FILE =====
    def upload(self):
        file = filedialog.askopenfilename()
        if file:
            self.df = load_data(file)
            self.file_label.config(text=file.split("/")[-1])
            self.update_kpis()  # 🔥 update KPI after upload

    # ===== UI =====
    def clear_charts(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

    def show_chart(self, fig):
        self.current_fig = fig
        canvas = FigureCanvasTkAgg(fig, master=self.scrollable_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, pady=10)

    # ===== EXPORT =====
    def export_png(self):
        if self.current_fig:
            file = filedialog.asksaveasfilename(defaultextension=".png")
            if file:
                self.current_fig.savefig(file)

    def export_pdf(self):
        if self.current_fig:
            file = filedialog.asksaveasfilename(defaultextension=".pdf")
            if file:
                self.current_fig.savefig(file)

    # ===== REPORTS =====
    def show_orders(self):
        if self.df is None:
            return

        self.clear_charts()
        analyzer = SalesAnalyzer(self.df)
        analyzer.clean_data()

        data = analyzer.orders_by_date()
        fig = Figure(figsize=(10, 4))
        ax = fig.add_subplot(111)

        data.plot(ax=ax)
        ax.set_title("Orders by Date")
        ax.tick_params(axis='x', rotation=45)

        fig.tight_layout()
        self.show_chart(fig)

    def show_products(self):
        if self.df is None:
            return

        self.clear_charts()
        analyzer = SalesAnalyzer(self.df)
        analyzer.clean_data()

        data = analyzer.product_sales().head(10)
        fig = Figure(figsize=(8, max(4, len(data)*0.6)))
        ax = fig.add_subplot(111)

        data.sort_values().plot(kind='barh', ax=ax)
        ax.set_title("Top Products")

        fig.tight_layout()
        self.show_chart(fig)

    def show_locations(self):
        if self.df is None:
            return

        self.clear_charts()
        analyzer = SalesAnalyzer(self.df)
        analyzer.clean_data()

        data = analyzer.location_sales().head(10)
        fig = Figure(figsize=(8, max(4, len(data)*0.6)))
        ax = fig.add_subplot(111)

        data.sort_values().plot(kind='barh', ax=ax)
        ax.set_title("Top Locations")

        fig.tight_layout()
        self.show_chart(fig)

    def show_payment(self):
        if self.df is None:
            return

        self.clear_charts()
        analyzer = SalesAnalyzer(self.df)
        analyzer.clean_data()

        fig = Figure(figsize=(6, 4))
        ax = fig.add_subplot(111)

        analyzer.payment_type().plot(kind='pie', ax=ax, autopct='%1.1f%%')
        ax.set_title("Payment Type")

        self.show_chart(fig)

    def show_discount(self):
        if self.df is None:
            return

        self.clear_charts()
        analyzer = SalesAnalyzer(self.df)
        analyzer.clean_data()

        fig = Figure(figsize=(6, 4))
        ax = fig.add_subplot(111)

        analyzer.discount_usage().head(5).plot(kind='pie', ax=ax, autopct='%1.1f%%')
        ax.set_title("Discount Usage")

        self.show_chart(fig)

    def show_vendor(self):
        if self.df is None:
            return

        self.clear_charts()
        analyzer = SalesAnalyzer(self.df)
        analyzer.clean_data()

        data = analyzer.vendor_sales().head(10)
        fig = Figure(figsize=(8, max(4, len(data)*0.6)))
        ax = fig.add_subplot(111)

        data.sort_values().plot(kind='barh', ax=ax)
        ax.set_title("Vendor Sales")

        fig.tight_layout()
        self.show_chart(fig)