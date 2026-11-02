import tkinter as tk
from tkinter import ttk, messagebox


class ProductForm:
    def __init__(self, parent, product_manager, on_save=None, mode="add"):
        self.parent = parent
        self.product_manager = product_manager
        self.on_save = on_save
        self.mode = mode
        self.current_product_id = None

        self.form_frame = tk.Frame(self.parent, bg="#ECF0F1")
        self.form_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self._build_widgets()

    def _build_widgets(self):
        title_text = "Add Product" if self.mode == "add" else "Update Product"
        header = tk.Label(
            self.form_frame,
            text=title_text,
            font=("Segoe UI", 20, "bold"),
            bg="#ECF0F1",
            fg="#2C3E50",
            anchor="w",
        )
        header.pack(fill=tk.X, pady=(0, 20))

        card = tk.Frame(self.form_frame, bg="white", relief=tk.FLAT, bd=1, padx=30, pady=25)
        card.pack(fill=tk.X)

        form_container = tk.Frame(card, bg="white")
        form_container.pack(fill=tk.X)

        for i in range(2):
            form_container.grid_columnconfigure(i, weight=1, pad=20)

        self.entries = {}

        fields = [
            ("Product Name", "product_name", "entry", 0, 0),
            ("Category", "category", "combobox", 1, 0),
            ("Quantity", "quantity", "entry", 0, 1),
            ("Price", "price", "entry", 1, 1),
            ("Supplier", "supplier", "entry", 0, 2),
            ("Minimum Stock Level", "minimum_stock", "entry", 1, 2),
        ]

        for label_text, field_key, field_type, col, row in fields:
            row_frame = tk.Frame(form_container, bg="white")
            row_frame.grid(row=row, column=col, sticky="ew", padx=10, pady=12)

            label = tk.Label(
                row_frame,
                text=label_text,
                font=("Segoe UI", 10, "bold"),
                bg="white",
                fg="#34495E",
                anchor="w",
            )
            label.pack(fill=tk.X, pady=(0, 5))

            if field_type == "combobox":
                categories = self.product_manager.get_product_categories_list()
                var = tk.StringVar()
                entry = ttk.Combobox(
                    row_frame,
                    textvariable=var,
                    values=categories,
                    font=("Segoe UI", 11),
                    state="readonly",
                )
                entry.pack(fill=tk.X, ipady=4)
                self.entries[field_key] = {"widget": entry, "var": var}
            else:
                var = tk.StringVar()
                entry = tk.Entry(
                    row_frame,
                    textvariable=var,
                    font=("Segoe UI", 11),
                    relief=tk.FLAT,
                    bg="#F8F9FA",
                    bd=1,
                    highlightthickness=1,
                    highlightbackground="#BDC3C7",
                    highlightcolor="#3498DB",
                )
                entry.pack(fill=tk.X, ipady=5)
                self.entries[field_key] = {"widget": entry, "var": var}

        btn_frame = tk.Frame(card, bg="white")
        btn_frame.pack(fill=tk.X, pady=(25, 0))

        right_btns = tk.Frame(btn_frame, bg="white")
        right_btns.pack(side=tk.RIGHT)

        btn_text = "Add Product" if self.mode == "add" else "Update Product"
        save_btn = tk.Button(
            right_btns,
            text=btn_text,
            font=("Segoe UI", 11, "bold"),
            bg="#3498DB",
            fg="white",
            relief=tk.FLAT,
            padx=25,
            pady=10,
            cursor="hand2",
            activebackground="#2980B9",
            activeforeground="white",
            command=self._on_save,
        )
        save_btn.pack(side=tk.RIGHT, padx=(10, 0))

        clear_btn = tk.Button(
            right_btns,
            text="Clear",
            font=("Segoe UI", 11),
            bg="#95A5A6",
            fg="white",
            relief=tk.FLAT,
            padx=25,
            pady=10,
            cursor="hand2",
            activebackground="#7F8C8D",
            activeforeground="white",
            command=self._on_clear,
        )
        clear_btn.pack(side=tk.RIGHT)

    def _get_form_values(self):
        return {
            "product_name": self.entries["product_name"]["var"].get().strip(),
            "category": self.entries["category"]["var"].get().strip(),
            "quantity": self.entries["quantity"]["var"].get().strip(),
            "price": self.entries["price"]["var"].get().strip(),
            "supplier": self.entries["supplier"]["var"].get().strip(),
            "minimum_stock": self.entries["minimum_stock"]["var"].get().strip(),
        }

    def _on_save(self):
        values = self._get_form_values()

        if self.mode == "add":
            result = self.product_manager.add_product(
                values["product_name"],
                values["category"],
                values["quantity"],
                values["price"],
                values["supplier"],
                values["minimum_stock"],
            )
        else:
            if self.current_product_id is None:
                messagebox.showerror("Error", "No product selected for update.")
                return
            result = self.product_manager.update_product(
                self.current_product_id,
                values["product_name"],
                values["category"],
                values["quantity"],
                values["price"],
                values["supplier"],
                values["minimum_stock"],
            )

        if result["success"]:
            if self.mode == "add":
                messagebox.showinfo("Success", "Product added successfully!")
                self._on_clear()
            else:
                messagebox.showinfo("Success", "Product updated successfully!")
            if self.on_save:
                self.on_save()
        else:
            error_msg = "\n".join(result["errors"])
            messagebox.showerror("Validation Error", error_msg)

    def _on_clear(self):
        for key in self.entries:
            self.entries[key]["var"].set("")

    def load_product(self, product_id):
        product = self.product_manager.get_product(product_id)
        if product is None:
            return

        self.current_product_id = product_id
        self.entries["product_name"]["var"].set(product["product_name"])
        self.entries["category"]["var"].set(product["category"])
        self.entries["quantity"]["var"].set(str(product["quantity"]))
        self.entries["price"]["var"].set(str(product["price"]))
        self.entries["supplier"]["var"].set(product["supplier"])
        self.entries["minimum_stock"]["var"].set(str(product["minimum_stock"]))

    def set_mode(self, mode):
        self.mode = mode
        title_text = "Add Product" if mode == "add" else "Update Product"
        for widget in self.form_frame.winfo_children():
            if isinstance(widget, tk.Label) and widget.cget("text") in ("Add Product", "Update Product"):
                widget.config(text=title_text)
                break
        for child in self.form_frame.winfo_children():
            if isinstance(child, tk.Frame):
                for grandchild in child.winfo_children():
                    if isinstance(grandchild, tk.Frame):
                        for btn in grandchild.winfo_children():
                            for sub_btn in btn.winfo_children():
                                if isinstance(sub_btn, tk.Button) and sub_btn.cget("text") in (
                                    "Add Product",
                                    "Update Product",
                                ):
                                    btn_text = "Add Product" if mode == "add" else "Update Product"
                                    sub_btn.config(text=btn_text)
                                    break

    def show(self):
        self.form_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        if self.mode == "add":
            self._on_clear()

    def hide(self):
        self.form_frame.pack_forget()
