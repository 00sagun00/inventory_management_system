import tkinter as tk
from tkinter import messagebox

from product_manager import ProductManager
from dashboard import Dashboard
from product_form import ProductForm
from product_list import ProductList, LowStockList, Reports


NAV_COLOR = "#2C3E50"
NAV_HOVER = "#34495E"
NAV_ACTIVE = "#3498DB"
CONTENT_BG = "#ECF0F1"
TEXT_LIGHT = "#ECF0F1"


class InventoryManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.root.geometry("1200x750")
        self.root.minsize(1000, 650)
        self.root.configure(bg=CONTENT_BG)

        self.product_manager = ProductManager()
        self.current_view = None
        self.nav_buttons = {}

        self._build_styles()
        self._build_main_layout()
        self._build_views()
        self._show_dashboard()

    def _build_styles(self):
        pass

    def _build_main_layout(self):
        self.sidebar = tk.Frame(self.root, bg=NAV_COLOR, width=220)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        logo_frame = tk.Frame(self.sidebar, bg=NAV_COLOR, pady=25, padx=15)
        logo_frame.pack(fill=tk.X)

        tk.Label(
            logo_frame,
            text="INVENTORY",
            font=("Segoe UI", 16, "bold"),
            bg=NAV_COLOR,
            fg=TEXT_LIGHT,
            anchor="w",
        ).pack(fill=tk.X)
        tk.Label(
            logo_frame,
            text="Management System",
            font=("Segoe UI", 9),
            bg=NAV_COLOR,
            fg="#BDC3C7",
            anchor="w",
        ).pack(fill=tk.X)

        tk.Frame(self.sidebar, bg="#1A252F", height=1).pack(fill=tk.X, padx=15, pady=15)

        nav_container = tk.Frame(self.sidebar, bg=NAV_COLOR)
        nav_container.pack(fill=tk.BOTH, expand=True, padx=10)

        nav_items = [
            ("dashboard", "Dashboard", "1", self._show_dashboard),
            ("products", "Products", "2", self._show_products),
            ("add", "Add Product", "3", self._show_add_product),
            ("low_stock", "Low Stock", "4", self._show_low_stock),
            ("reports", "Reports", "5", self._show_reports),
        ]

        for key, label_text, shortcut, command in nav_items:
            btn = self._create_nav_button(nav_container, label_text, shortcut, command, key)
            btn.pack(fill=tk.X, pady=3, ipady=10)
            self.nav_buttons[key] = btn

        nav_spacer = tk.Frame(nav_container, bg=NAV_COLOR)
        nav_spacer.pack(fill=tk.BOTH, expand=True)

        exit_btn = self._create_nav_button(
            nav_container, "Exit", "Esc", self._on_exit, "exit", is_exit=True
        )
        exit_btn.pack(fill=tk.X, pady=3, ipady=10)
        self.nav_buttons["exit"] = exit_btn

        version_frame = tk.Frame(self.sidebar, bg=NAV_COLOR, padx=15, pady=15)
        version_frame.pack(fill=tk.X, side=tk.BOTTOM)
        tk.Label(
            version_frame,
            text="Version 1.0",
            font=("Segoe UI", 8),
            bg=NAV_COLOR,
            fg="#7F8C8D",
            anchor="w",
        ).pack(fill=tk.X)

        self.content_area = tk.Frame(self.root, bg=CONTENT_BG)
        self.content_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.root.bind("<Alt-KeyPress-1>", lambda e: self._show_dashboard())
        self.root.bind("<Alt-KeyPress-2>", lambda e: self._show_products())
        self.root.bind("<Alt-KeyPress-3>", lambda e: self._show_add_product())
        self.root.bind("<Alt-KeyPress-4>", lambda e: self._show_low_stock())
        self.root.bind("<Alt-KeyPress-5>", lambda e: self._show_reports())
        self.root.bind("<Escape>", lambda e: self._on_exit())

    def _create_nav_button(self, parent, text, shortcut, command, key, is_exit=False):
        frame = tk.Frame(parent, bg=NAV_COLOR, highlightthickness=0)

        btn_bg = NAV_COLOR
        text_fg = "#BDC3C7" if not is_exit else "#E74C3C"

        label = tk.Label(
            frame,
            text=text,
            font=("Segoe UI", 11),
            bg=btn_bg,
            fg=text_fg,
            anchor="w",
            padx=15,
            cursor="hand2",
        )
        label.pack(fill=tk.X, expand=True, side=tk.LEFT)

        shortcut_label = tk.Label(
            frame,
            text=shortcut,
            font=("Segoe UI", 9, "bold"),
            bg=btn_bg,
            fg="#7F8C8D",
            padx=10,
            cursor="hand2",
        )
        shortcut_label.pack(side=tk.RIGHT)

        for widget in (frame, label, shortcut_label):
            widget.bind("<Enter>", lambda e: self._on_nav_enter(key, is_exit))
            widget.bind("<Leave>", lambda e: self._on_nav_leave(key))
            widget.bind("<Button-1>", lambda e: command())

        frame._is_active = False
        frame._widgets = (label, shortcut_label)
        frame._bg_normal = NAV_COLOR
        frame._bg_hover = NAV_HOVER if not is_exit else "#C0392B"
        frame._fg_normal = text_fg
        frame._fg_hover = TEXT_LIGHT
        frame._key = key

        return frame

    def _on_nav_enter(self, key, is_exit=False):
        if key not in self.nav_buttons:
            return
        frame = self.nav_buttons[key]
        if frame._is_active:
            return
        for w in frame._widgets:
            w.config(bg=frame._bg_hover)
            if isinstance(w, tk.Label) and w.cget("text") != frame._key and len(w.cget("text")) > 3:
                w.config(fg=frame._fg_hover)

    def _on_nav_leave(self, key):
        if key not in self.nav_buttons:
            return
        frame = self.nav_buttons[key]
        if frame._is_active:
            return
        for w in frame._widgets:
            w.config(bg=frame._bg_normal)
            if isinstance(w, tk.Label) and len(w.cget("text")) > 3:
                w.config(fg=frame._fg_normal)

    def _set_active_nav(self, active_key):
        for key, frame in self.nav_buttons.items():
            if key == active_key:
                frame._is_active = True
                for w in frame._widgets:
                    w.config(bg=NAV_ACTIVE, fg=TEXT_LIGHT)
            else:
                frame._is_active = False
                if key == "exit":
                    for w in frame._widgets:
                        w.config(bg=NAV_COLOR)
                        if isinstance(w, tk.Label) and len(w.cget("text")) > 3:
                            w.config(fg="#E74C3C" if w == frame._widgets[0] else "#7F8C8D")
                else:
                    for w in frame._widgets:
                        w.config(bg=NAV_COLOR)
                        if isinstance(w, tk.Label) and len(w.cget("text")) > 3:
                            w.config(fg="#BDC3C7" if w == frame._widgets[0] else "#7F8C8D")

    def _build_views(self):
        self.dashboard = Dashboard(self.content_area, self.product_manager)

        self.product_list = ProductList(
            self.content_area,
            self.product_manager,
            on_update=self._handle_update_product,
            on_delete=self._refresh_dashboard,
        )

        self.product_form = ProductForm(
            self.content_area,
            self.product_manager,
            on_save=self._on_product_saved,
        )

        self.low_stock_list = LowStockList(self.content_area, self.product_manager)
        self.reports = Reports(self.content_area, self.product_manager)

        self._hide_all_views()

    def _hide_all_views(self):
        self.dashboard.hide()
        self.product_list.hide()
        self.product_form.hide()
        self.low_stock_list.hide()
        self.reports.hide()

    def _show_dashboard(self):
        self._hide_all_views()
        self.dashboard.show()
        self.current_view = "dashboard"
        self._set_active_nav("dashboard")

    def _show_products(self):
        self._hide_all_views()
        self.product_list.show()
        self.current_view = "products"
        self._set_active_nav("products")

    def _show_add_product(self):
        self._hide_all_views()
        self.product_form.set_mode("add")
        self.product_form.show()
        self.current_view = "add"
        self._set_active_nav("add")

    def _show_low_stock(self):
        self._hide_all_views()
        self.low_stock_list.show()
        self.current_view = "low_stock"
        self._set_active_nav("low_stock")

    def _show_reports(self):
        self._hide_all_views()
        self.reports.show()
        self.current_view = "reports"
        self._set_active_nav("reports")

    def _handle_update_product(self, product_id):
        self._hide_all_views()
        self.product_form.set_mode("update")
        self.product_form.load_product(product_id)
        self.product_form.show()
        self.current_view = "add"
        self._set_active_nav("add")

    def _on_product_saved(self):
        self._refresh_dashboard()
        if self.product_form.mode == "update":
            self._show_products()

    def _refresh_dashboard(self):
        self.dashboard.refresh()

    def _on_exit(self):
        confirm = messagebox.askyesno(
            "Exit Application",
            "Are you sure you want to exit the Inventory Management System?",
        )
        if confirm:
            self.root.destroy()


def main():
    root = tk.Tk()

    try:
        root.iconbitmap(default="")
    except Exception:
        pass

    app = InventoryManagementApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
