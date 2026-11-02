import tkinter as tk
from tkinter import ttk


class Dashboard:
    def __init__(self, parent, product_manager):
        self.parent = parent
        self.product_manager = product_manager

        self.dashboard_frame = tk.Frame(self.parent, bg="#ECF0F1")
        self.dashboard_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self._build_widgets()

    def _build_widgets(self):
        header = tk.Label(
            self.dashboard_frame,
            text="Dashboard",
            font=("Segoe UI", 20, "bold"),
            bg="#ECF0F1",
            fg="#2C3E50",
            anchor="w",
        )
        header.pack(fill=tk.X, pady=(0, 15))

        stats_frame = tk.Frame(self.dashboard_frame, bg="#ECF0F1")
        stats_frame.pack(fill=tk.X, pady=(0, 15))

        self.stat_cards = {}
        stat_configs = [
            ("Total Products", "#3498DB", "total_products"),
            ("Total Stock", "#9B59B6", "total_stock"),
            ("Inventory Value", "#1ABC9C", "inventory_value"),
            ("Low Stock", "#F39C12", "low_stock_count"),
            ("Out of Stock", "#E74C3C", "out_of_stock_count"),
        ]

        for i, (label, color, key) in enumerate(stat_configs):
            card = tk.Frame(stats_frame, bg=color, padx=15, pady=15)
            card.grid(row=0, column=i, padx=5, sticky="nsew")
            stats_frame.grid_columnconfigure(i, weight=1)

            lbl_label = tk.Label(
                card,
                text=label,
                font=("Segoe UI", 10),
                bg=color,
                fg="white",
            )
            lbl_label.pack(anchor="w")

            lbl_value = tk.Label(
                card,
                text="0",
                font=("Segoe UI", 18, "bold"),
                bg=color,
                fg="white",
            )
            lbl_value.pack(anchor="w", pady=(5, 0))

            self.stat_cards[key] = lbl_value

        content_frame = tk.Frame(self.dashboard_frame, bg="#ECF0F1")
        content_frame.pack(fill=tk.BOTH, expand=True)
        content_frame.grid_columnconfigure(0, weight=3)
        content_frame.grid_columnconfigure(1, weight=2)
        content_frame.grid_rowconfigure(0, weight=1)

        recent_frame = tk.Frame(content_frame, bg="white", relief=tk.FLAT, bd=1)
        recent_frame.grid(row=0, column=0, padx=(0, 5), sticky="nsew")

        recent_header = tk.Label(
            recent_frame,
            text="Recent Products",
            font=("Segoe UI", 14, "bold"),
            bg="white",
            fg="#2C3E50",
            anchor="w",
            padx=15,
            pady=12,
        )
        recent_header.pack(fill=tk.X)

        ttk.Separator(recent_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=15)

        tree_container = tk.Frame(recent_frame, bg="white", padx=10, pady=10)
        tree_container.pack(fill=tk.BOTH, expand=True)

        columns = ("Product", "Category", "Qty", "Price", "Status")
        self.recent_tree = ttk.Treeview(
            tree_container, columns=columns, show="headings", height=8
        )

        self.recent_tree.heading("Product", text="Product")
        self.recent_tree.heading("Category", text="Category")
        self.recent_tree.heading("Qty", text="Qty")
        self.recent_tree.heading("Price", text="Price")
        self.recent_tree.heading("Status", text="Status")

        self.recent_tree.column("Product", width=150)
        self.recent_tree.column("Category", width=130)
        self.recent_tree.column("Qty", width=60, anchor="center")
        self.recent_tree.column("Price", width=90, anchor="e")
        self.recent_tree.column("Status", width=110, anchor="center")

        scrollbar = ttk.Scrollbar(tree_container, orient=tk.VERTICAL, command=self.recent_tree.yview)
        self.recent_tree.configure(yscrollcommand=scrollbar.set)

        self.recent_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        low_stock_frame = tk.Frame(content_frame, bg="white", relief=tk.FLAT, bd=1)
        low_stock_frame.grid(row=0, column=1, padx=(5, 0), sticky="nsew")

        low_stock_header = tk.Label(
            low_stock_frame,
            text="Low Stock Products",
            font=("Segoe UI", 14, "bold"),
            bg="white",
            fg="#E67E22",
            anchor="w",
            padx=15,
            pady=12,
        )
        low_stock_header.pack(fill=tk.X)

        ttk.Separator(low_stock_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=15)

        low_tree_container = tk.Frame(low_stock_frame, bg="white", padx=10, pady=10)
        low_tree_container.pack(fill=tk.BOTH, expand=True)

        low_columns = ("Product", "Qty", "Min Stock")
        self.low_stock_tree = ttk.Treeview(
            low_tree_container, columns=low_columns, show="headings", height=8
        )

        self.low_stock_tree.heading("Product", text="Product")
        self.low_stock_tree.heading("Qty", text="Qty")
        self.low_stock_tree.heading("Min Stock", text="Min Stock")

        self.low_stock_tree.column("Product", width=150)
        self.low_stock_tree.column("Qty", width=60, anchor="center")
        self.low_stock_tree.column("Min Stock", width=80, anchor="center")

        low_scrollbar = ttk.Scrollbar(low_tree_container, orient=tk.VERTICAL, command=self.low_stock_tree.yview)
        self.low_stock_tree.configure(yscrollcommand=low_scrollbar.set)

        self.low_stock_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        low_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self._configure_tree_styles()

    def _configure_tree_styles(self):
        style = ttk.Style()
        style.configure(
            "Dashboard.Treeview",
            font=("Segoe UI", 9),
            rowheight=25,
            background="white",
            fieldbackground="white",
        )
        style.configure(
            "Dashboard.Treeview.Heading",
            font=("Segoe UI", 9, "bold"),
            background="#BDC3C7",
            foreground="#2C3E50",
        )
        self.recent_tree.configure(style="Dashboard.Treeview")
        self.low_stock_tree.configure(style="Dashboard.Treeview")

    def refresh(self):
        stats = self.product_manager.get_statistics()

        self.stat_cards["total_products"].config(text=str(stats["total_products"]))
        self.stat_cards["total_stock"].config(text=str(stats["total_stock"]))
        self.stat_cards["inventory_value"].config(
            text=self.product_manager.format_currency(stats["inventory_value"])
        )
        self.stat_cards["low_stock_count"].config(text=str(stats["low_stock_count"]))
        self.stat_cards["out_of_stock_count"].config(text=str(stats["out_of_stock_count"]))

        for item in self.recent_tree.get_children():
            self.recent_tree.delete(item)

        recent_products = self.product_manager.get_recent_products(8)
        for product in recent_products:
            status = self.product_manager.get_stock_status(
                product["quantity"], product["minimum_stock"]
            )
            self.recent_tree.insert(
                "",
                tk.END,
                values=(
                    product["product_name"],
                    product["category"],
                    product["quantity"],
                    self.product_manager.format_currency(product["price"]),
                    status,
                ),
            )

        for item in self.low_stock_tree.get_children():
            self.low_stock_tree.delete(item)

        low_stock_products = self.product_manager.get_low_stock_products()
        for product in low_stock_products:
            self.low_stock_tree.insert(
                "",
                tk.END,
                values=(
                    product["product_name"],
                    product["quantity"],
                    product["minimum_stock"],
                ),
            )

    def show(self):
        self.dashboard_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.refresh()

    def hide(self):
        self.dashboard_frame.pack_forget()
