import sqlite3
import os
from datetime import datetime


DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "inventory.db")


def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT NOT NULL,
            category TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            supplier TEXT NOT NULL,
            minimum_stock INTEGER NOT NULL,
            date_added TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def add_product(product_name, category, quantity, price, supplier, minimum_stock):
    conn = get_connection()
    cursor = conn.cursor()

    date_added = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO products (product_name, category, quantity, price, supplier, minimum_stock, date_added)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (product_name, category, quantity, price, supplier, minimum_stock, date_added))

    product_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return product_id


def get_products():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products ORDER BY date_added DESC")
    rows = cursor.fetchall()

    products = [dict(row) for row in rows]

    conn.close()
    return products


def get_product_by_id(product_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    row = cursor.fetchone()

    product = dict(row) if row else None

    conn.close()
    return product


def update_product(product_id, product_name, category, quantity, price, supplier, minimum_stock):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE products
        SET product_name = ?, category = ?, quantity = ?, price = ?, supplier = ?, minimum_stock = ?
        WHERE id = ?
    """, (product_name, category, quantity, price, supplier, minimum_stock, product_id))

    conn.commit()
    affected = cursor.rowcount
    conn.close()

    return affected > 0


def delete_product(product_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))

    conn.commit()
    affected = cursor.rowcount
    conn.close()

    return affected > 0


def search_products(search_term, search_by="name"):
    conn = get_connection()
    cursor = conn.cursor()

    search_pattern = f"%{search_term}%"

    if search_by == "name":
        cursor.execute("SELECT * FROM products WHERE product_name LIKE ? ORDER BY date_added DESC", (search_pattern,))
    elif search_by == "category":
        cursor.execute("SELECT * FROM products WHERE category LIKE ? ORDER BY date_added DESC", (search_pattern,))
    elif search_by == "supplier":
        cursor.execute("SELECT * FROM products WHERE supplier LIKE ? ORDER BY date_added DESC", (search_pattern,))
    else:
        cursor.execute("""
            SELECT * FROM products
            WHERE product_name LIKE ? OR category LIKE ? OR supplier LIKE ?
            ORDER BY date_added DESC
        """, (search_pattern, search_pattern, search_pattern))

    rows = cursor.fetchall()
    products = [dict(row) for row in rows]

    conn.close()
    return products


def get_products_by_category(category):
    conn = get_connection()
    cursor = conn.cursor()

    if category == "All Categories":
        cursor.execute("SELECT * FROM products ORDER BY date_added DESC")
    else:
        cursor.execute("SELECT * FROM products WHERE category = ? ORDER BY date_added DESC", (category,))

    rows = cursor.fetchall()
    products = [dict(row) for row in rows]

    conn.close()
    return products


def get_low_stock_products():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM products
        WHERE quantity <= minimum_stock
        ORDER BY quantity ASC
    """)

    rows = cursor.fetchall()
    products = [dict(row) for row in rows]

    conn.close()
    return products


def get_out_of_stock_products():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products WHERE quantity = 0")

    rows = cursor.fetchall()
    products = [dict(row) for row in rows]

    conn.close()
    return products


def get_inventory_statistics():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) as count FROM products")
    total_products = cursor.fetchone()["count"]

    cursor.execute("SELECT COALESCE(SUM(quantity), 0) as total FROM products")
    total_stock = cursor.fetchone()["total"]

    cursor.execute("SELECT quantity, price FROM products")
    rows = cursor.fetchall()
    inventory_value = sum(row["quantity"] * row["price"] for row in rows)

    cursor.execute("""
        SELECT COUNT(*) as count FROM products
        WHERE quantity <= minimum_stock AND quantity > 0
    """)
    low_stock_count = cursor.fetchone()["count"]

    cursor.execute("SELECT COUNT(*) as count FROM products WHERE quantity = 0")
    out_of_stock_count = cursor.fetchone()["count"]

    most_expensive = None
    cheapest = None

    if total_products > 0:
        cursor.execute("SELECT product_name, price FROM products ORDER BY price DESC LIMIT 1")
        row = cursor.fetchone()
        most_expensive = {"product_name": row["product_name"], "price": row["price"]}

        cursor.execute("SELECT product_name, price FROM products ORDER BY price ASC LIMIT 1")
        row = cursor.fetchone()
        cheapest = {"product_name": row["product_name"], "price": row["price"]}

    conn.close()

    return {
        "total_products": total_products,
        "total_stock": total_stock,
        "inventory_value": inventory_value,
        "low_stock_count": low_stock_count,
        "out_of_stock_count": out_of_stock_count,
        "most_expensive": most_expensive,
        "cheapest": cheapest,
    }


def get_recent_products(limit=5):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products ORDER BY date_added DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    products = [dict(row) for row in rows]

    conn.close()
    return products


def get_categories():
    return [
        "All Categories",
        "Electronics",
        "Computer Accessories",
        "Stationery",
        "Clothing",
        "Grocery",
        "Furniture",
        "Other",
    ]


def get_product_categories():
    return [
        "Electronics",
        "Computer Accessories",
        "Stationery",
        "Clothing",
        "Grocery",
        "Furniture",
        "Other",
    ]


def insert_sample_data():
    sample_products = [
        ("Laptop", "Electronics", 10, 55000, "ABC Computers", 3),
        ("Keyboard", "Computer Accessories", 20, 800, "XYZ Electronics", 5),
        ("Mouse", "Computer Accessories", 30, 500, "XYZ Electronics", 5),
        ("Notebook", "Stationery", 50, 80, "Stationery World", 10),
        ("Pen", "Stationery", 100, 10, "Stationery World", 20),
    ]

    for product in sample_products:
        try:
            add_product(*product)
        except Exception:
            pass
