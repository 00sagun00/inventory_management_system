import tkinter as tk
from tkinter import ttk, messagebox


class ProductList:
    def __init__(self, parent, product_manager, on_update=None, on_delete=None):
        self.parent = parent
        self.product_manager = product_manager
        self.on_update = on_update
        self.on_delete = on_delete
        self.current_products = []

        self.list_frame = tk.Frame(self.parent, bg="#ECF0F1")
        self.list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self._build_widgets()

    def _build_widgets(self):
        header = tk.Label(
            self.list_frame,
            text="Products",
            font=("Segoe UI", 20, "bold"),
            bg="#ECF0F1",
            fg="#2C3E50",
            anchor="w",
        )
        header.pack(fill=tk.X, pady=(0, 15))

        toolbar = tk.Frame(self.list_frame, bg="#ECF0F1")
        toolbar.pack(fill=tk.X, pady=(0, 10))

        search_frame = tk.Frame(toolbar, bg="#ECF0F1")
        search_frame.pack(side=tk.LEFT)

        tk.Label(
            search_frame,
            text="Search:",
            font=("Segoe UI", 10, "bold"),
            bg="#ECF0F1",
            fg="#34495E",
        ).pack(side=tk.LEFT, padx=(0, 5))

        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=("Segoe UI", 10),
            width=25,
            relief=tk.FLAT,
            bg="white",
            bd=1,
            highlightthickness=1,
            highlightbackground="#BDC3C7",
            highlightcolor="#3498DB",
        )
        self.search_entry.pack(side=tk.LEFT, ipady=3, padx=(0, 5))

        self.search_by_var = tk.StringVar(value="All")
        search_by = ttk.Combobox(
            search_frame,
            textvariable=self.search_by_var,
            values=["All", "Product Name", "Category", "Supplier"],
            font=("Segoe UI", 10),
            state="readonly",
            width=14,
        )
        search_by.pack(side=tk.LEFT, padx=(0, 5), ipady=3)

        search_btn = tk.Button(
            search_frame,
            text="Search",
            font=("Segoe UI", 10, "bold"),
            bg="#27AE60",
            fg="white",
            relief=tk.FLAT,
            padx=18,
            pady=3,
            cursor="hand2",
            activebackground="#229954",
            activeforeground="white",
            command=self._on_search,
        )
        search_btn.pack(side=tk.LEFT, padx=(0, 5))

        clear_search_btn = tk.Button(
            search_frame,
            text="Clear Search",
            font=("Segoe UI", 10),
            bg="#95A5A6",
            fg="white",
            relief=tk.FLAT,
            padx=15,
            pady=3,
            cursor="hand2",
            activebackground="#7F8C8D",
            activeforeground="white",
            command=self._on_clear_search,
        )
        clear_search_btn.pack(side=tk.LEFT)

        filter_frame = tk.Frame(toolbar, bg="#ECF0F1")
        filter_frame.pack(side=tk.LEFT, padx=(30, 0))

        tk.Label(
            filter_frame,
            text="Category:",
            font=("Segoe UI", 10, "bold"),
            bg="#ECF0F1",
            fg="#34495E",
        ).pack(side=tk.LEFT, padx=(0, 5))

        self.category_var = tk.StringVar(value="All Categories")
        categories = self.product_manager.get_categories_list()
        category_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.category_var,
            values=categories,
            font=("Segoe UI", 10),
            state="readonly",
            width=18,
        )
        category_combo.pack(side=tk.LEFT, ipady=3)
        category_combo.bind("<<ComboboxSelected>>", lambda e: self._on_category_filter())

        btn_frame = tk.Frame(toolbar, bg="#ECF0F1")
        btn_frame.pack(side=tk.RIGHT)

        refresh_btn = tk.Button(
            btn_frame,
            text="Refresh",
            font=("Segoe UI", 10),
            bg="#3498DB",
            fg="white",
            relief=tk.FLAT,
            padx=15,
            pady=3,
            cursor="hand2",
            activebackground="#2980B9",
            activeforeground="white",
            command=self.refresh,
        )
        refresh_btn.pack(side=tk.RIGHT, padx=(5, 0))

        delete_btn = tk.Button(
            btn_frame,
            text="Delete Product",
            font=("Segoe UI", 10),
            bg="#E74C3C",
            fg="white",
            relief=tk.FLAT,
            padx=15,
            pady=3,
            cursor="hand2",
            activebackground="#C0392B",
            activeforeground="white",
            command=self._on_delete,
        )
        delete_btn.pack(side=tk.RIGHT, padx=(5, 0))

        update_btn = tk.Button(
            btn_frame,
            text="Update Product",
            font=("Segoe UI", 10),
            bg="#F39C12",
            fg="white",
            relief=tk.FLAT,
            padx=15,
            pady=3,
            cursor="hand2",
            activebackground="#D68910",
            activeforeground="white",
            command=self._on_update,
        )
        update_btn.pack(side=tk.RIGHT, padx=(5, 0))

        table_card = tk.Frame(self.list_frame, bg="white", relief=tk.FLAT, bd=1)
        table_card.pack(fill=tk.BOTH, expand=True)

        table_container = tk.Frame(table_card, bg="white", padx=10, pady=10)
        table_container.pack(fill=tk.BOTH, expand=True)

        columns = (
            "ID",
            "Product Name",
            "Category",
            "Quantity",
            "Price",
            "Supplier",
            "Min Stock",
            "Date Added",
            "Status",
        )
        self.product_tree = ttk.Treeview(
            table_container, columns=columns, show="headings"
        )

        col_widths = [50, 180, 140, 70, 100, 140, 80, 130, 110]
        for col, width in zip(columns, col_widths):
            self.product_tree.heading(col, text=col)
            anchor = "w"
            if col in ("ID", "Quantity", "Min Stock"):
                anchor = "center"
            elif col in ("Price",):
                anchor = "e"
            self.product_tree.column(col, width=width, anchor=anchor)

        tree_scrollbar_y = ttk.Scrollbar(
            table_container, orient=tk.VERTICAL, command=self.product_tree.yview
        )
        self.product_tree.configure(yscrollcommand=tree_scrollbar_y.set)

        tree_scrollbar_x = ttk.Scrollbar(
            table_container, orient=tk.HORIZONTAL, command=self.product_tree.xview
        )
        self.product_tree.configure(xscrollcommand=tree_scrollbar_x.set)

        self.product_tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        tree_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y, after=self.product_tree)
        tree_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        self._configure_tree_styles()

    def _configure_tree_styles(self):
        style = ttk.Style()
        style.configure(
            "ProductList.Treeview",
            font=("Segoe UI", 9),
            rowheight=28,
            background="white",
            fieldbackground="white",
        )
        style.configure(
            "ProductList.Treeview.Heading",
            font=("Segoe UI", 9, "bold"),
            background="#34495E",
            foreground="white",
        )
        style.map(
            "ProductList.Treeview",
            background=[("selected", "#3498DB")],
            foreground=[("selected", "white")],
        )
        self.product_tree.configure(style="ProductList.Treeview")

    def _populate_table(self, products):
        for item in self.product_tree.get_children():
            self.product_tree.delete(item)

        self.current_products = products

        for product in products:
            status = self.product_manager.get_stock_status(
                product["quantity"], product["minimum_stock"]
            )
            self.product_tree.insert(
                "",
                tk.END,
                iid=str(product["id"]),
                values=(
                    product["id"],
                    product["product_name"],
                    product["category"],
                    product["quantity"],
                    self.product_manager.format_currency(product["price"]),
                    product["supplier"],
                    product["minimum_stock"],
                    product["date_added"],
                    status,
                ),
            )

        self._color_status_rows()

    def _color_status_rows(self):
        for product in self.current_products:
            color = self.product_manager.get_stock_status_color(
                product["quantity"], product["minimum_stock"]
            )
            item_id = str(product["id"])
            self.product_tree.tag_configure(item_id, foreground=color)
            try:
                self.product_tree.item(item_id, tags=(item_id,))
            except Exception:
                pass

    def _get_selected_product_id(self):
        selected = self.product_tree.selection()
        if not selected:
            return None
        return int(selected[0])

    def _on_search(self):
        search_term = self.search_var.get()
        search_by = self.search_by_var.get()

        if not search_term.strip():
            self.refresh()
            return

        search_map = {
            "All": "all",
            "Product Name": "name",
            "Category": "category",
            "Supplier": "supplier",
        }
        search_key = search_map.get(search_by, "all")
        products = self.product_manager.search_products(search_term, search_key)
        self._populate_table(products)

    def _on_clear_search(self):
        self.search_var.set("")
        self.category_var.set("All Categories")
        self.refresh()

    def _on_category_filter(self):
        category = self.category_var.get()
        products = self.product_manager.filter_by_category(category)
        self._populate_table(products)

    def _on_update(self):
        product_id = self._get_selected_product_id()
        if product_id is None:
            messagebox.showwarning("No Selection", "Please select a product to update.")
            return
        if self.on_update:
            self.on_update(product_id)

    def _on_delete(self):
        product_id = self._get_selected_product_id()
        if product_id is None:
            messagebox.showwarning("No Selection", "Please select a product to delete.")
            return

        product = self.product_manager.get_product(product_id)
        if product is None:
            messagebox.showerror("Error", "Product not found.")
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete this product?\n\n"
            f"Product: {product['product_name']}\n"
            f"ID: {product['id']}",
        )

        if confirm:
            deleted = self.product_manager.delete_product(product_id)
            if deleted:
                messagebox.showinfo("Deleted", "Product deleted successfully!")
                self.refresh()
                if self.on_delete:
                    self.on_delete()
            else:
                messagebox.showerror("Error", "Failed to delete product.")

    def refresh(self):
        products = self.product_manager.get_all_products()
        self._populate_table(products)

    def show(self):
        self.list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.refresh()

    def hide(self):
        self.list_frame.pack_forget()


class LowStockList:
    def __init__(self, parent, product_manager):
        self.parent = parent
        self.product_manager = product_manager

        self.low_stock_frame = tk.Frame(self.parent, bg="#ECF0F1")
        self.low_stock_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self._build_widgets()

    def _build_widgets(self):
        header = tk.Label(
            self.low_stock_frame,
            text="Low Stock Products",
            font=("Segoe UI", 20, "bold"),
            bg="#ECF0F1",
            fg="#E67E22",
            anchor="w",
        )
        header.pack(fill=tk.X, pady=(0, 15))

        summary_card = tk.Frame(self.low_stock_frame, bg="#F39C12", padx=20, pady=15)
        summary_card.pack(fill=tk.X, pady=(0, 15))

        tk.Label(
            summary_card,
            text="Products with quantity at or below minimum stock level",
            font=("Segoe UI", 11),
            bg="#F39C12",
            fg="white",
        ).pack(side=tk.LEFT)

        self.count_label = tk.Label(
            summary_card,
            text="0 products",
            font=("Segoe UI", 14, "bold"),
            bg="#F39C12",
            fg="white",
        )
        self.count_label.pack(side=tk.RIGHT)

        table_card = tk.Frame(self.low_stock_frame, bg="white", relief=tk.FLAT, bd=1)
        table_card.pack(fill=tk.BOTH, expand=True)

        table_container = tk.Frame(table_card, bg="white", padx=10, pady=10)
        table_container.pack(fill=tk.BOTH, expand=True)

        columns = (
            "ID",
            "Product Name",
            "Category",
            "Quantity",
            "Minimum Stock",
            "Status",
            "Supplier",
            "Price",
            "Inventory Value",
        )
        self.low_stock_tree = ttk.Treeview(
            table_container, columns=columns, show="headings"
        )

        col_widths = [50, 180, 140, 80, 100, 120, 140, 100, 120]
        for col, width in zip(columns, col_widths):
            self.low_stock_tree.heading(col, text=col)
            anchor = "w"
            if col in ("ID", "Quantity", "Minimum Stock"):
                anchor = "center"
            elif col in ("Price", "Inventory Value"):
                anchor = "e"
            self.low_stock_tree.column(col, width=width, anchor=anchor)

        tree_scrollbar_y = ttk.Scrollbar(
            table_container, orient=tk.VERTICAL, command=self.low_stock_tree.yview
        )
        self.low_stock_tree.configure(yscrollcommand=tree_scrollbar_y.set)

        tree_scrollbar_x = ttk.Scrollbar(
            table_container, orient=tk.HORIZONTAL, command=self.low_stock_tree.xview
        )
        self.low_stock_tree.configure(xscrollcommand=tree_scrollbar_x.set)

        self.low_stock_tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        tree_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y, after=self.low_stock_tree)
        tree_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        style = ttk.Style()
        style.configure(
            "LowStock.Treeview",
            font=("Segoe UI", 9),
            rowheight=28,
            background="white",
            fieldbackground="white",
        )
        style.configure(
            "LowStock.Treeview.Heading",
            font=("Segoe UI", 9, "bold"),
            background="#E67E22",
            foreground="white",
        )
        style.map(
            "LowStock.Treeview",
            background=[("selected", "#F39C12")],
            foreground=[("selected", "white")],
        )
        self.low_stock_tree.configure(style="LowStock.Treeview")

    def refresh(self):
        for item in self.low_stock_tree.get_children():
            self.low_stock_tree.delete(item)

        products = self.product_manager.get_low_stock_products()
        self.count_label.config(text=f"{len(products)} product(s)")

        for product in products:
            status = self.product_manager.get_stock_status(
                product["quantity"], product["minimum_stock"]
            )
            inv_value = self.product_manager.calculate_inventory_value(
                product["quantity"], product["price"]
            )
            self.low_stock_tree.insert(
                "",
                tk.END,
                values=(
                    product["id"],
                    product["product_name"],
                    product["category"],
                    product["quantity"],
                    product["minimum_stock"],
                    status,
                    product["supplier"],
                    self.product_manager.format_currency(product["price"]),
                    self.product_manager.format_currency(inv_value),
                ),
            )

    def show(self):
        self.low_stock_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.refresh()

    def hide(self):
        self.low_stock_frame.pack_forget()


class Reports:
    def __init__(self, parent, product_manager):
        self.parent = parent
        self.product_manager = product_manager

        self.reports_frame = tk.Frame(self.parent, bg="#ECF0F1")
        self.reports_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self._build_widgets()

    def _build_widgets(self):
        header = tk.Label(
            self.reports_frame,
            text="Inventory Reports",
            font=("Segoe UI", 20, "bold"),
            bg="#ECF0F1",
            fg="#2C3E50",
            anchor="w",
        )
        header.pack(fill=tk.X, pady=(0, 20))

        report_card = tk.Frame(self.reports_frame, bg="white", relief=tk.FLAT, bd=1, padx=30, pady=25)
        report_card.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            report_card,
            text="INVENTORY REPORT",
            font=("Segoe UI", 16, "bold"),
            bg="white",
            fg="#2C3E50",
        ).pack(anchor="w", pady=(0, 15))

        ttk.Separator(report_card, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=(0, 20))

        content_frame = tk.Frame(report_card, bg="white")
        content_frame.pack(fill=tk.BOTH, expand=True)

        left_col = tk.Frame(content_frame, bg="white")
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 30))

        right_col = tk.Frame(content_frame, bg="white")
        right_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(30, 0))

        self.report_labels = {}

        left_items = [
            ("Total Products:", "total_products"),
            ("Total Stock:", "total_stock"),
            ("Inventory Value:", "inventory_value"),
            ("Low Stock Products:", "low_stock_count"),
            ("Out of Stock Products:", "out_of_stock_count"),
        ]

        for label_text, key in left_items:
            row = tk.Frame(left_col, bg="white")
            row.pack(fill=tk.X, pady=8)

            tk.Label(
                row,
                text=label_text,
                font=("Segoe UI", 11, "bold"),
                bg="white",
                fg="#34495E",
                width=22,
                anchor="w",
            ).pack(side=tk.LEFT)

            lbl = tk.Label(
                row,
                text="0",
                font=("Segoe UI", 12),
                bg="white",
                fg="#2C3E50",
                anchor="w",
            )
            lbl.pack(side=tk.LEFT)
            self.report_labels[key] = lbl

        tk.Label(
            right_col,
            text="Most Expensive Product:",
            font=("Segoe UI", 11, "bold"),
            bg="white",
            fg="#34495E",
            anchor="w",
        ).pack(anchor="w", pady=(8, 5))

        self.most_expensive_label = tk.Label(
            right_col,
            text="-",
            font=("Segoe UI", 12, "bold"),
            bg="#F8F9FA",
            fg="#E74C3C",
            anchor="w",
            padx=15,
            pady=12,
            relief=tk.FLAT,
        )
        self.most_expensive_label.pack(fill=tk.X, pady=(0, 20))

        tk.Label(
            right_col,
            text="Cheapest Product:",
            font=("Segoe UI", 11, "bold"),
            bg="white",
            fg="#34495E",
            anchor="w",
        ).pack(anchor="w", pady=(8, 5))

        self.cheapest_label = tk.Label(
            right_col,
            text="-",
            font=("Segoe UI", 12, "bold"),
            bg="#F8F9FA",
            fg="#27AE60",
            anchor="w",
            padx=15,
            pady=12,
            relief=tk.FLAT,
        )
        self.cheapest_label.pack(fill=tk.X)

        bottom_frame = tk.Frame(report_card, bg="white")
        bottom_frame.pack(fill=tk.X, pady=(30, 0))

        refresh_btn = tk.Button(
            bottom_frame,
            text="Refresh Report",
            font=("Segoe UI", 11, "bold"),
            bg="#3498DB",
            fg="white",
            relief=tk.FLAT,
            padx=25,
            pady=8,
            cursor="hand2",
            activebackground="#2980B9",
            activeforeground="white",
            command=self.refresh,
        )
        refresh_btn.pack(side=tk.RIGHT)

    def refresh(self):
        stats = self.product_manager.get_statistics()

        self.report_labels["total_products"].config(text=str(stats["total_products"]))
        self.report_labels["total_stock"].config(text=str(stats["total_stock"]))
        self.report_labels["inventory_value"].config(
            text=self.product_manager.format_currency(stats["inventory_value"])
        )
        self.report_labels["low_stock_count"].config(text=str(stats["low_stock_count"]))
        self.report_labels["out_of_stock_count"].config(text=str(stats["out_of_stock_count"]))

        if stats["most_expensive"]:
            me = stats["most_expensive"]
            self.most_expensive_label.config(
                text=f"{me['product_name']} - {self.product_manager.format_currency(me['price'])}"
            )
        else:
            self.most_expensive_label.config(text="No products available")

        if stats["cheapest"]:
            ch = stats["cheapest"]
            self.cheapest_label.config(
                text=f"{ch['product_name']} - {self.product_manager.format_currency(ch['price'])}"
            )
        else:
            self.cheapest_label.config(text="No products available")

    def show(self):
        self.reports_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.refresh()

    def hide(self):
        self.reports_frame.pack_forget()
