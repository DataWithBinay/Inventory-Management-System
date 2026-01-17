import sqlite3
import os
import csv
from datetime import datetime

class Database:
    def __init__(self):
        self.db_file = 'inventory.db'
        self._create_tables()

    def _create_tables(self):
        """Create database tables if they don't exist"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        # Create products table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                quantity INTEGER NOT NULL
            )
        ''')

        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL
            )
        ''')

        # Create sales table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                total REAL NOT NULL,
                date TEXT NOT NULL,
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')

        # Insert default data if tables are empty
        cursor.execute('SELECT COUNT(*) FROM products')
        if cursor.fetchone()[0] == 0:
            cursor.executemany('''
                INSERT INTO products (id, name, price, quantity) VALUES (?, ?, ?, ?)
            ''', [
                ('1', 'Apple', 2.0, 50),
                ('2', 'Banana', 1.5, 30),
                ('3', 'Orange', 3.0, 20)
            ])

        cursor.execute('SELECT COUNT(*) FROM users')
        if cursor.fetchone()[0] == 0:
            cursor.executemany('''
                INSERT INTO users (username, password) VALUES (?, ?)
            ''', [
                ('admin', '8a5dd8dc906d9fa12f1d9e46f8edfa07a64be30dd731eb7451fa6edd61f929c5:97f10bd3de95d0d0f6989cf6a4cb6f9a4c206d3335b376dc2c1e950f5242bffa'),
                ('user', '5e98fb5678aa3327b4f5a67ef1106c488c73b7545c86d86a34faceee61a0f520:0f2ba4e250ba1978eb6431420052c473faf07d2918449d13bc9c20e3e72b5531')
            ])

        conn.commit()
        conn.close()

    def get_products(self):
        """Get all products"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, price, quantity FROM products')
        rows = cursor.fetchall()
        conn.close()
        return [{'id': row[0], 'name': row[1], 'price': row[2], 'quantity': row[3]} for row in rows]

    def save_products(self, products):
        """Save all products (replace existing)"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM products')
        cursor.executemany('''
            INSERT INTO products (id, name, price, quantity) VALUES (?, ?, ?, ?)
        ''', [(p['id'], p['name'], p['price'], p['quantity']) for p in products])
        conn.commit()
        conn.close()

    def get_users(self):
        """Get all users"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT username, password FROM users')
        rows = cursor.fetchall()
        conn.close()
        return [{'username': row[0], 'password': row[1]} for row in rows]

    def save_users(self, users):
        """Save all users (replace existing)"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM users')
        cursor.executemany('''
            INSERT INTO users (username, password) VALUES (?, ?)
        ''', [(u['username'], u['password']) for u in users])
        conn.commit()
        conn.close()

    def get_sales(self):
        """Get all sales"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT id, product_id, quantity, total, date FROM sales')
        rows = cursor.fetchall()
        conn.close()
        return [{'id': row[0], 'product_id': row[1], 'quantity': row[2], 'total': row[3], 'date': row[4]} for row in rows]

    def add_sale(self, product_id, quantity, total):
        """Add a sale record"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('''
            INSERT INTO sales (product_id, quantity, total, date) VALUES (?, ?, ?, ?)
        ''', (product_id, quantity, total, date))
        conn.commit()
        conn.close()

    def update_product_quantity(self, product_id, new_quantity):
        """Update product quantity"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('UPDATE products SET quantity = ? WHERE id = ?', (new_quantity, product_id))
        conn.commit()
        conn.close()

    def add_product(self, product_id, name, price, quantity):
        """Add a new product"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO products (id, name, price, quantity) VALUES (?, ?, ?, ?)
            ''', (product_id, name, price, quantity))
            conn.commit()
            success = True
        except sqlite3.IntegrityError:
            success = False
        conn.close()
        return success

    def add_user(self, username, password):
        """Add a new user"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO users (username, password) VALUES (?, ?)
            ''', (username, password))
            conn.commit()
            success = True
        except sqlite3.IntegrityError:
            success = False
        conn.close()
        return success

    def update_user_password(self, username, new_password):
        """Update user password"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET password = ? WHERE username = ?', (new_password, username))
        conn.commit()
        conn.close()
        return cursor.rowcount > 0

    def export_sales_report_csv(self, filename='sales_report.csv'):
        """Export comprehensive sales report to CSV"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        # Get sales with product names
        cursor.execute('''
            SELECT s.id, s.product_id, p.name, s.quantity, s.total, s.date
            FROM sales s
            JOIN products p ON s.product_id = p.id
            ORDER BY s.date DESC
        ''')

        sales_data = cursor.fetchall()
        conn.close()

        # Write to CSV
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Sale_ID', 'Product_ID', 'Product_Name', 'Quantity_Sold', 'Total_Amount', 'Sale_Date']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for sale in sales_data:
                writer.writerow({
                    'Sale_ID': sale[0],
                    'Product_ID': sale[1],
                    'Product_Name': sale[2],
                    'Quantity_Sold': sale[3],
                    'Total_Amount': f"{sale[4]:.2f}",
                    'Sale_Date': sale[5]
                })

        return filename, len(sales_data)

    def export_sales_summary_csv(self, filename='sales_summary.csv'):
        """Export sales summary report with statistics"""
        summary = self.get_sales_summary()

        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)

            # Write summary header
            writer.writerow(['SALES SUMMARY REPORT'])
            writer.writerow(['Generated on', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
            writer.writerow([])

            # Overall statistics
            writer.writerow(['OVERALL STATISTICS'])
            writer.writerow(['Total Sales Amount', f"Rs.{summary['total_sales_amount']:.2f}"])
            writer.writerow(['Total Items Sold', summary['total_items_sold']])
            writer.writerow([])

            # Top selling products
            writer.writerow(['TOP SELLING PRODUCTS'])
            writer.writerow(['Product Name', 'Quantity Sold', 'Total Amount'])
            for product in summary['top_products']:
                writer.writerow([product[0], product[1], f"Rs.{product[2]:.2f}"])
            writer.writerow([])

            # Daily sales
            writer.writerow(['DAILY SALES SUMMARY'])
            writer.writerow(['Date', 'Items Sold', 'Total Amount'])
            for daily in summary['daily_sales']:
                writer.writerow([daily[0], daily[1], f"Rs.{daily[2]:.2f}"])

        return filename

    def get_sales_summary(self):
        """Get sales summary statistics"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        # Total sales amount
        cursor.execute('SELECT SUM(total) FROM sales')
        total_sales = cursor.fetchone()[0] or 0

        # Total items sold
        cursor.execute('SELECT SUM(quantity) FROM sales')
        total_items = cursor.fetchone()[0] or 0

        # Best selling products
        cursor.execute('''
            SELECT p.name, SUM(s.quantity) as total_qty, SUM(s.total) as total_amount
            FROM sales s
            JOIN products p ON s.product_id = p.id
            GROUP BY s.product_id, p.name
            ORDER BY total_qty DESC
            LIMIT 5
        ''')
        top_products = cursor.fetchall()

        # Sales by date
        cursor.execute('''
            SELECT DATE(date) as sale_date, SUM(quantity) as daily_qty, SUM(total) as daily_total
            FROM sales
            GROUP BY DATE(date)
            ORDER BY sale_date DESC
        ''')
        daily_sales = cursor.fetchall()

        conn.close()

        return {
            'total_sales_amount': total_sales,
            'total_items_sold': total_items,
            'top_products': top_products,
            'daily_sales': daily_sales
        }