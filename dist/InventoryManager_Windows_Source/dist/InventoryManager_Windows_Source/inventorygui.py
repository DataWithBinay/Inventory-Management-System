from tkinter import *
from tkinter import messagebox
from user_manager import UserManager
from inventory_manager import InventoryManager
from sales_manager import SalesManager

def center_window(root, w=400, h=220):
    root.update_idletasks()
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    root.geometry(f"{w}x{h}+{x}+{y}")

class InventoryGUI:
    def __init__(self, inventory):
        self.inventory = inventory
        # Initialize managers
        self.user_manager = UserManager()
        self.inventory_manager = InventoryManager()
        self.sales_manager = SalesManager()
        self.current_user = None       
        center_window(self.inventory, 1000, 800)
        # self.inventory.attributes('-fullscreen', True)
        self.inventory.title("Inventory Management System")

        # Create container frame
        container = Frame(self.inventory, bg="white")
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}

        # Create all pages and stack them
        for F in (HomePage, InventoryPage, RegisterPage, ForgotPasswordPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(HomePage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class HomePage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        # Title Label
        title = Label(self, text="Inventory Management System",
                      font=("Times New Roman", 30), bg="lightblue")
        title.place(x=0, y=0, relwidth=1)
        #username label
        username_label = Label(self, text="Username:", font=("Times New Roman", 16), bg="white")
        username_label.place(x=300, y=300, width=150, height=40)

        self.username_entry = Entry(self, font=("Times New Roman", 16), bg="lightblue")
        self.username_entry.place(x=500, y=300, width=300, height=40)

        #password label
        password_label = Label(self, text="Password:", font=("Times New Roman", 16), bg="white")
        password_label.place(x=300, y=400, width=150, height=40)

        self.password_entry = Entry(self, font=("Times New Roman", 16), bg="lightblue", show="*")
        self.password_entry.place(x=500, y=400, width=300, height=40)

        # Forgot password link
        forgot_link = Label(self, text="Forgot Password?", font=("Times New Roman", 16, "underline"),
                            fg="blue", cursor="hand2", bg="white")
        forgot_link.place(x=650, y=600)
        forgot_link.bind("<Button-1>", lambda e: controller.show_frame(ForgotPasswordPage))

        # Navigation buttons
        login_button = Button(self, text="Login", font=("Times New Roman", 16), bg="lightblue",
                              command=self.login)
        login_button.place(x=600, y=500, width=200, height=40)
        # Register password link 
        register_button = Label(self, text="If new user, Register", font=("Times New Roman", 16, "underline"), bg="white",
                                 fg="blue", cursor="hand2")
        register_button.place(x=500, y=200, width=300, height=40)
        register_button.bind("<Button-1>", lambda e: controller.show_frame(RegisterPage))

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.controller.user_manager.authenticate(username, password):
            self.controller.current_user = username
            self.controller.show_frame(InventoryPage)
            # Clear fields
            self.username_entry.delete(0, END)
            self.password_entry.delete(0, END)
        else:
            messagebox.showerror("Error", "Invalid username or password")

class InventoryPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        
        # Get products from database
        self.products = self.controller.inventory_manager.get_products()
        self.cart = self.controller.sales_manager.cart
        
        # Title
        title = Label(self, text="Inventory Management System", font=("Times New Roman", 30), bg="lightblue")
        title.pack(fill="x", pady=10)
        
        # Search section
        search_frame = Frame(self, bg="white")
        search_frame.pack(fill="x", padx=20, pady=10)
        
        Label(search_frame, text="Search by ID or Name:", font=("Times New Roman", 14), bg="white").pack(side="left")
        self.search_entry = Entry(search_frame, font=("Times New Roman", 14), width=30)
        self.search_entry.pack(side="left", padx=10)
        self.search_entry.bind("<KeyRelease>", self.search_products)
        
        # Main content frame
        content_frame = Frame(self, bg="white")
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Left panel - Product management
        left_panel = Frame(content_frame, bg="lightgray", width=400)
        left_panel.pack(side="left", fill="y", padx=10)
        
        # Add Product Section
        add_frame = LabelFrame(left_panel, text="Add Product", font=("Times New Roman", 16), bg="lightgray")
        add_frame.pack(fill="x", padx=10, pady=10)
        
        Label(add_frame, text="ID:", bg="lightgray").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.add_id = Entry(add_frame, width=20)
        self.add_id.grid(row=0, column=1, padx=5, pady=5)
        
        Label(add_frame, text="Name:", bg="lightgray").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.add_name = Entry(add_frame, width=20)
        self.add_name.grid(row=1, column=1, padx=5, pady=5)
        
        Label(add_frame, text="Price:", bg="lightgray").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.add_price = Entry(add_frame, width=20)
        self.add_price.grid(row=2, column=1, padx=5, pady=5)
        
        Label(add_frame, text="Quantity:", bg="lightgray").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.add_quantity = Entry(add_frame, width=20)
        self.add_quantity.grid(row=3, column=1, padx=5, pady=5)
        
        Button(add_frame, text="Add Product", bg="green", fg="white", command=self.add_product).grid(row=4, column=0, columnspan=2, pady=10)
        
        # Sales Section
        sales_frame = LabelFrame(left_panel, text="Sales", font=("Times New Roman", 16), bg="lightgray")
        sales_frame.pack(fill="x", padx=10, pady=10)
        
        Label(sales_frame, text="Product ID:", bg="lightgray").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.sales_id = Entry(sales_frame, width=20)
        self.sales_id.grid(row=0, column=1, padx=5, pady=5)
        
        Label(sales_frame, text="Quantity:", bg="lightgray").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.sales_quantity = Entry(sales_frame, width=20)
        self.sales_quantity.grid(row=1, column=1, padx=5, pady=5)
        
        Button(sales_frame, text="Add to Cart", bg="blue", fg="white", command=self.add_to_cart).grid(row=2, column=0, columnspan=2, pady=10)
        
        # Billing Button
        Button(left_panel, text="Generate Bill", bg="red", fg="white", font=("Times New Roman", 16), command=self.generate_bill).pack(pady=10)
        
        # Export Sales Report Button
        Button(left_panel, text="Export Sales Report", bg="green", fg="white", font=("Times New Roman", 14), command=self.export_sales_report).pack(pady=5)
        
        # Export Sales Summary Button
        Button(left_panel, text="Export Sales Summary", bg="orange", fg="white", font=("Times New Roman", 14), command=self.export_sales_summary).pack(pady=5)
        
        # Right panel - Product list
        right_panel = Frame(content_frame, bg="white")
        right_panel.pack(side="right", fill="both", expand=True, padx=10)
        
        Label(right_panel, text="Product List", font=("Times New Roman", 18), bg="white").pack(pady=10)
        
        # Product listbox with scrollbar
        list_frame = Frame(right_panel)
        list_frame.pack(fill="both", expand=True)
        
        scrollbar = Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.product_listbox = Listbox(list_frame, font=("Times New Roman", 12), yscrollcommand=scrollbar.set, width=50, height=20)
        self.product_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.product_listbox.yview)
        
        self.update_product_list()
        
        # Back button
        back_link = Label(self, text="← Logout", font=("Times New Roman", 12, "underline"),
                          fg="blue", cursor="hand2", bg="white")
        back_link.pack(anchor="nw", padx=20, pady=10)
        back_link.bind("<Button-1>", self.logout)
    
    def logout(self, event=None):
        self.controller.current_user = None
        self.controller.sales_manager.clear_cart()
        self.controller.show_frame(HomePage)
    
    def update_product_list(self, filtered_products=None):
        self.product_listbox.delete(0, END)
        products = filtered_products if filtered_products else self.controller.inventory_manager.get_products()
        for product in products:
            self.product_listbox.insert(END, f"ID: {product['id']} | Name: {product['name']} | Price: Rs.{product['price']} | Qty: {product['quantity']}")
    
    def search_products(self, event):
        query = self.search_entry.get().lower()
        if not query:
            self.update_product_list()
            return
        filtered = self.controller.inventory_manager.search_products(query)
        self.update_product_list(filtered)
    
    def add_product(self):
        try:
            product_id = self.add_id.get()
            name = self.add_name.get()
            price = float(self.add_price.get())
            quantity = int(self.add_quantity.get())
            
            if not all([product_id, name]):
                messagebox.showerror("Error", "Please fill all fields")
                return
            
            success, message = self.controller.inventory_manager.add_product(product_id, name, price, quantity)
            if success:
                self.update_product_list()
                # Clear fields
                self.add_id.delete(0, END)
                self.add_name.delete(0, END)
                self.add_price.delete(0, END)
                self.add_quantity.delete(0, END)
                messagebox.showinfo("Success", message)
            else:
                messagebox.showerror("Error", message)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid price and quantity")
    
    def add_to_cart(self):
        product_id = self.sales_id.get()
        try:
            quantity = int(self.sales_quantity.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid quantity")
            return
        
        success, message = self.controller.sales_manager.add_to_cart(product_id, quantity)
        if success:
            self.update_product_list()
            self.sales_id.delete(0, END)
            self.sales_quantity.delete(0, END)
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", message)
    
    def generate_bill(self):
        success, result = self.controller.sales_manager.generate_bill()
        if not success:
            messagebox.showwarning("Warning", result)
            return
        
        # Create billing window
        bill_window = Toplevel(self)
        bill_window.title("Bill")
        center_window(bill_window, 600, 400)
        
        Label(bill_window, text="BILL", font=("Times New Roman", 24, "bold")).pack(pady=10)
        
        # Bill content
        bill_frame = Frame(bill_window)
        bill_frame.pack(fill="both", expand=True, padx=20)
        
        # Items
        items_text = Text(bill_frame, font=("Times New Roman", 12), height=10)
        items_text.pack(fill="both", expand=True)
        
        items_text.insert(END, "Items Purchased:\n\n")
        for item in result['items']:
            product = item['product']
            qty = item['quantity']
            total = product['price'] * qty
            items_text.insert(END, f"{product['name']} (x{qty}) - Rs.{total:.2f}\n")
        
        items_text.insert(END, f"\nSubtotal: Rs.{result['subtotal']:.2f}")
        items_text.insert(END, f"\nVAT (13%): Rs.{result['vat']:.2f}")
        items_text.insert(END, f"\nTotal: Rs.{result['total']:.2f}")
        
        items_text.config(state="disabled")
        
        Button(bill_window, text="Close", command=bill_window.destroy).pack(pady=10)
    
    def export_sales_report(self):
        """Export sales report to CSV file"""
        try:
            filename, record_count = self.controller.inventory_manager.db.export_sales_report_csv()
            messagebox.showinfo("Success", f"Sales report exported to '{filename}'\n{record_count} sales records exported.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export sales report: {str(e)}")
    
    def export_sales_summary(self):
        """Export sales summary report to CSV file"""
        try:
            filename = self.controller.inventory_manager.db.export_sales_summary_csv()
            messagebox.showinfo("Success", f"Sales summary exported to '{filename}'")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export sales summary: {str(e)}")
        
        
class RegisterPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        # Title
        title = Label(self, text="Register New User", font=("Times New Roman", 30), bg="lightblue")
        title.place(x=0, y=0, relwidth=1)

        # Username
        username_label = Label(self, text="Username:", font=("Times New Roman", 16), bg="white")
        username_label.place(x=300, y=300, width=150, height=40)

        self.username_entry = Entry(self, font=("Times New Roman", 16), bg="lightblue")
        self.username_entry.place(x=500, y=300, width=300, height=40)

        # Password
        password_label = Label(self, text="Password:", font=("Times New Roman", 16), bg="white")
        password_label.place(x=300, y=400, width=150, height=40)

        self.password_entry = Entry(self, font=("Times New Roman", 16), bg="lightblue", show="*")
        self.password_entry.place(x=500, y=400, width=300, height=40)

        # Register button
        register_button = Button(self, text="Register", font=("Times New Roman", 16), bg="lightblue",
                                command=self.register)
        register_button.place(x=600, y=500, width=200, height=40)

        # Back to login
        back_link = Label(self, text="← Back to Login", font=("Times New Roman", 12, "underline"),
                          fg="blue", cursor="hand2", bg="white")
        back_link.place(x=50, y=50)
        back_link.bind("<Button-1>", lambda e: controller.show_frame(HomePage))

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if not username or not password:
            messagebox.showerror("Error", "Please fill all fields")
            return
        success, message = self.controller.user_manager.register_user(username, password)
        if success:
            messagebox.showinfo("Success", message)
            self.controller.show_frame(HomePage)
            # Clear fields
            self.username_entry.delete(0, END)
            self.password_entry.delete(0, END)
        else:
            messagebox.showerror("Error", message)
         

class ForgotPasswordPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        # Title
        title = Label(self, text="Forgot Password", font=("Times New Roman", 30), bg="lightblue")
        title.place(x=0, y=0, relwidth=1)

        # Email/Username
        email_label = Label(self, text="Email/Username:", font=("Times New Roman", 16), bg="white")
        email_label.place(x=250, y=300, width=200, height=40)

        self.email_entry = Entry(self, font=("Times New Roman", 16), bg="lightblue")
        self.email_entry.place(x=500, y=300, width=300, height=40)

        # Reset button
        reset_button = Button(self, text="Reset Password", font=("Times New Roman", 16), bg="lightblue",command=self.show_reset_form)
        reset_button.place(x=600, y=400, width=200, height=40)

        # Back to login
        back_link = Label(self, text="← Back to Login", font=("Times New Roman", 12, "underline"),
                          fg="blue", cursor="hand2", bg="white")
        back_link.place(x=50, y=50)
        back_link.bind("<Button-1>", lambda e: controller.show_frame(HomePage))

        # New password fields (initially hidden)
        self.new_password_label = Label(self, text="New Password", font=("Times New Roman", 16), bg="white")
        self.new_password_entry = Entry(self, font=("Times New Roman", 16), bg="lightblue", show="*")
        
        self.confirm_password_label = Label(self, text="Confirm Password:", font=("Times New Roman", 16), bg="white")
        self.confirm_password_entry = Entry(self, font=("Times New Roman", 16), bg="lightblue", show="*")

        self.submit_button = Button(self, text="Submit", font=("Times New Roman", 16), bg="lightblue", command=self.reset_password)

    def show_reset_form(self):
        username = self.email_entry.get()
        if not username:
            messagebox.showerror("Error", "Please enter username")
            return
        
        # Check if user exists
        users = self.controller.user_manager.db.get_users()
        user_exists = any(user['username'] == username for user in users)
        if not user_exists:
            messagebox.showerror("Error", "User not found")
            return

        # Show password reset fields
        self.new_password_label.place(x=250, y=200, width=200, height=40)
        self.new_password_entry.place(x=500, y=200, width=300, height=40)
        
        self.confirm_password_label.place(x=250, y=300, width=200, height=40)
        self.confirm_password_entry.place(x=500, y=300, width=300, height=40)

        self.submit_button.place(x=600, y=400, width=200, height=40)

    def reset_password(self):
        username = self.email_entry.get()
        new_password = self.new_password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        
        if new_password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        success, message = self.controller.user_manager.reset_password(username, new_password)
        if success:
            messagebox.showinfo("Success", message)
            self.controller.show_frame(HomePage)
            # Clear and hide fields
            self.email_entry.delete(0, END)
            self.new_password_entry.delete(0, END)
            self.confirm_password_entry.delete(0, END)
            self.new_password_label.place_forget()
            self.new_password_entry.place_forget()
            self.confirm_password_label.place_forget()
            self.confirm_password_entry.place_forget()
            self.submit_button.place_forget()
        else:
            messagebox.showerror("Error", message)
inventory = Tk()
app = InventoryGUI(inventory)
inventory.mainloop()