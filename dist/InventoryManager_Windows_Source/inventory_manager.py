from database import Database

class InventoryManager:
    def __init__(self):
        self.db = Database()

    def get_products(self):
        """Get all products"""
        products = self.db.get_products()
        # Convert string values to appropriate types
        for product in products:
            product['price'] = float(product['price'])
            product['quantity'] = int(product['quantity'])
        return products

    def add_product(self, product_id, name, price, quantity):
        """Add a new product"""
        if self.db.add_product(product_id, name, price, quantity):
            return True, "Product added successfully"
        else:
            return False, "Product ID already exists"

    def update_product_quantity(self, product_id, quantity_change):
        """Update product quantity (positive for add, negative for subtract)"""
        products = self.get_products()
        for product in products:
            if product['id'] == product_id:
                new_quantity = product['quantity'] + quantity_change
                if new_quantity < 0:
                    return False, "Insufficient stock"
                self.db.update_product_quantity(product_id, new_quantity)
                return True, "Quantity updated successfully"
        return False, "Product not found"

    def search_products(self, query):
        """Search products by ID or name"""
        products = self.get_products()
        query = query.lower()
        return [p for p in products if query in p['id'].lower() or query in p['name'].lower()]