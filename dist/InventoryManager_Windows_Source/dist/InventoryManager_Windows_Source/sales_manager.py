from database import Database
from inventory_manager import InventoryManager

class SalesManager:
    def __init__(self):
        self.db = Database()
        self.inventory = InventoryManager()
        self.cart = []

    def add_to_cart(self, product_id, quantity):
        """Add product to cart"""
        products = self.inventory.get_products()
        product = next((p for p in products if p['id'] == product_id), None)
        if not product:
            return False, "Product not found"
        if quantity > product['quantity']:
            return False, "Insufficient stock"
        self.cart.append({"product": product, "quantity": quantity})
        # Update inventory
        self.inventory.update_product_quantity(product_id, -quantity)
        return True, f"Added {quantity} {product['name']} to cart"

    def get_cart_total(self):
        """Calculate cart total"""
        subtotal = sum(item['product']['price'] * item['quantity'] for item in self.cart)
        vat_rate = 0.13  # 13% VAT
        vat = subtotal * vat_rate
        total = subtotal + vat
        return subtotal, vat, total

    def generate_bill(self):
        """Generate bill and save sales records"""
        if not self.cart:
            return False, "Cart is empty"

        subtotal, vat, total = self.get_cart_total()

        # Save each sale
        for item in self.cart:
            product = item['product']
            quantity = item['quantity']
            item_total = product['price'] * quantity
            self.db.add_sale(product['id'], quantity, item_total)

        # Clear cart
        cart_items = self.cart.copy()
        self.cart.clear()

        return True, {
            'items': cart_items,
            'subtotal': subtotal,
            'vat': vat,
            'total': total
        }

    def clear_cart(self):
        """Clear the cart without processing"""
        self.cart.clear()