from database import (
    add_product as db_add_product,
    get_products as db_get_products,
    get_product_by_id as db_get_product_by_id,
    update_product as db_update_product,
    delete_product as db_delete_product,
    search_products as db_search_products,
    get_products_by_category as db_get_products_by_category,
    get_low_stock_products as db_get_low_stock_products,
    get_out_of_stock_products as db_get_out_of_stock_products,
    get_inventory_statistics as db_get_inventory_statistics,
    get_recent_products as db_get_recent_products,
    init_database,
    insert_sample_data,
    get_categories,
    get_product_categories,
)


class ProductManager:
    def __init__(self):
        init_database()

    def validate_product_data(self, product_name, category, quantity, price, supplier, minimum_stock):
        errors = []

        if not product_name or not product_name.strip():
            errors.append("Please enter product name.")

        if not category or not category.strip():
            errors.append("Please select a category.")

        try:
            quantity = int(quantity)
            if quantity < 0:
                errors.append("Quantity must be greater than or equal to 0.")
        except (ValueError, TypeError):
            errors.append("Quantity must be a valid number.")

        try:
            price = float(price)
            if price < 0:
                errors.append("Price must be greater than or equal to 0.")
        except (ValueError, TypeError):
            errors.append("Price must be a valid number.")

        if not supplier or not supplier.strip():
            errors.append("Please enter supplier name.")

        try:
            minimum_stock = int(minimum_stock)
            if minimum_stock < 0:
                errors.append("Minimum stock must be greater than or equal to 0.")
        except (ValueError, TypeError):
            errors.append("Minimum stock must be a valid number.")

        return errors

    def add_product(self, product_name, category, quantity, price, supplier, minimum_stock):
        errors = self.validate_product_data(
            product_name, category, quantity, price, supplier, minimum_stock
        )

        if errors:
            return {"success": False, "errors": errors}

        try:
            product_id = db_add_product(
                product_name.strip(),
                category.strip(),
                int(quantity),
                float(price),
                supplier.strip(),
                int(minimum_stock),
            )
            return {"success": True, "product_id": product_id, "errors": []}
        except Exception as e:
            return {"success": False, "errors": [f"Database error: {str(e)}"]}

    def get_all_products(self):
        try:
            return db_get_products()
        except Exception as e:
            return []

    def get_product(self, product_id):
        try:
            return db_get_product_by_id(product_id)
        except Exception as e:
            return None

    def update_product(self, product_id, product_name, category, quantity, price, supplier, minimum_stock):
        errors = self.validate_product_data(
            product_name, category, quantity, price, supplier, minimum_stock
        )

        if errors:
            return {"success": False, "errors": errors}

        try:
            result = db_update_product(
                product_id,
                product_name.strip(),
                category.strip(),
                int(quantity),
                float(price),
                supplier.strip(),
                int(minimum_stock),
            )
            if result:
                return {"success": True, "errors": []}
            else:
                return {"success": False, "errors": ["Product not found."]}
        except Exception as e:
            return {"success": False, "errors": [f"Database error: {str(e)}"]}

    def delete_product(self, product_id):
        try:
            result = db_delete_product(product_id)
            return result
        except Exception as e:
            return False

    def search_products(self, search_term, search_by="all"):
        if not search_term or not search_term.strip():
            return self.get_all_products()

        try:
            return db_search_products(search_term.strip(), search_by)
        except Exception as e:
            return []

    def filter_by_category(self, category):
        try:
            return db_get_products_by_category(category)
        except Exception as e:
            return []

    def get_low_stock_products(self):
        try:
            return db_get_low_stock_products()
        except Exception as e:
            return []

    def get_out_of_stock_products(self):
        try:
            return db_get_out_of_stock_products()
        except Exception as e:
            return []

    def get_statistics(self):
        try:
            return db_get_inventory_statistics()
        except Exception as e:
            return {
                "total_products": 0,
                "total_stock": 0,
                "inventory_value": 0,
                "low_stock_count": 0,
                "out_of_stock_count": 0,
                "most_expensive": None,
                "cheapest": None,
            }

    def get_recent_products(self, limit=5):
        try:
            return db_get_recent_products(limit)
        except Exception as e:
            return []

    def get_stock_status(self, quantity, minimum_stock):
        if quantity == 0:
            return "OUT OF STOCK"
        elif quantity <= minimum_stock:
            return "LOW STOCK"
        else:
            return "IN STOCK"

    def get_stock_status_color(self, quantity, minimum_stock):
        if quantity == 0:
            return "#E74C3C"
        elif quantity <= minimum_stock:
            return "#F39C12"
        else:
            return "#27AE60"

    def calculate_inventory_value(self, quantity, price):
        return quantity * price

    def format_currency(self, amount):
        return f"\u20b9{amount:,.2f}"

    def get_categories_list(self):
        return get_categories()

    def get_product_categories_list(self):
        return get_product_categories()

    def load_sample_data(self):
        try:
            insert_sample_data()
            return True
        except Exception as e:
            return False
