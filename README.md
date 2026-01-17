# Inventory Management System

A complete inventory management system with graphical user interface, user authentication, and SQLite3 database storage.

## 🚀 **Desktop Application Available!**

**Standalone executable ready for distribution - no Python installation required!**

### For End Users (Recommended):
```bash
# Download: InventoryManager_v1.0_Linux.tar.gz
# Extract and install:
tar -xzf InventoryManager_v1.0_Linux.tar.gz
cd InventoryManager_v1.0_Linux
./install.sh
```

**What you get:**
- ✅ Standalone executable (13MB)
- ✅ Complete database with sample data
- ✅ Desktop shortcuts and menu integration
- ✅ All features: inventory, sales, reporting
- ✅ Cross-platform compatibility

**Package location:** `dist/InventoryManager_v1.0_Linux.tar.gz`

### 3. **Windows Users (Source Code)**
**Share with Windows friends:** `dist/InventoryManager_Windows_Source.zip`

**For Windows users:**
```cmd
# Download and extract the zip
# Double-click inventorygui.py
# Or run: python inventorygui.py
```

**What's included:**
- ✅ All Python source files
- ✅ SQLite database with sample data
- ✅ Simple README with instructions
- ✅ No Python installation needed (if using executable)

**Package location:** `dist/InventoryManager_Windows_Source.zip`

---

## Features

- **User Authentication**: Secure login system with PBKDF2 HMAC SHA256 password hashing
- **User Registration**: New user registration with secure password storage
- **Password Reset**: Forgot password functionality with secure hashing
- **Product Management**: Add new products, search products by ID or name
- **Sales Management**: Add products to cart, generate bills with VAT calculation
- **SQLite3 Database**: All data stored in a robust SQLite3 database with proper relationships and constraints
- **Modular Design**: Separate modules for database operations, user management, inventory, and sales

## Files Structure

- `inventorygui.py` - Main GUI application
- `database.py` - SQLite3 database operations
- `user_manager.py` - User authentication and registration
- `inventory_manager.py` - Product inventory operations
- `sales_manager.py` - Shopping cart and billing operations
- `inventory.db` - SQLite3 database file containing all data

## How to Run

1. Ensure Python 3.x is installed
2. Install required dependencies (tkinter is usually included with Python)
3. Run the application:
   ```bash
   python inventorygui.py
   ```

## Default Users

- Username: `admin`, Password: `admin123`
- Username: `user`, Password: `user123`

## Usage

1. **Login**: Use existing credentials or register a new account
2. **Add Products**: Use the "Add Product" section to add new inventory items
3. **Search Products**: Use the search bar to find products by ID or name
4. **Sales**: Enter product ID and quantity to add items to cart
5. **Generate Bill**: Click "Generate Bill" to process the sale and create a receipt
6. **Export Sales Report**: Click "Export Sales Report" to generate detailed CSV of all sales
7. **Export Sales Summary**: Click "Export Sales Summary" to generate analytics CSV

## SQLite3 Database

All data is stored in a single SQLite3 database file (`inventory.db`) with proper relational structure:

### Database Schema

```sql
-- Products table
CREATE TABLE products (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    quantity INTEGER NOT NULL
);

-- Users table
CREATE TABLE users (
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL
);

-- Sales table
CREATE TABLE sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    total REAL NOT NULL,
    date TEXT NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products (id)
);
```

### Database Benefits

- **Data Integrity**: Foreign key constraints ensure data consistency
- **Concurrent Access**: Multiple users can access the database simultaneously
- **ACID Compliance**: Atomic, Consistent, Isolated, Durable transactions
- **Performance**: Optimized queries and indexing capabilities
- **Backup**: Single file backup and restore
- **Cross-Platform**: Works on all operating systems

## CSV Export Features

The system provides comprehensive CSV export functionality for sales analysis:

### Sales Report CSV (`sales_report.csv`)
Contains detailed transaction data:
- `Sale_ID`: Unique transaction identifier
- `Product_ID`: Product identifier
- `Product_Name`: Full product name
- `Quantity_Sold`: Number of items sold
- `Total_Amount`: Total sale amount (Rs.)
- `Sale_Date`: Transaction timestamp

### Sales Summary CSV (`sales_summary.csv`)
Contains business analytics:
- **Overall Statistics**: Total sales amount and items sold
- **Top Selling Products**: Best performing products by quantity and revenue
- **Daily Sales Summary**: Sales performance by date

### Usage
1. Login to the inventory system
2. Click "Export Sales Report" for detailed transaction data
3. Click "Export Sales Summary" for business analytics
4. Open the generated CSV files in Excel, Google Sheets, or any spreadsheet application

## Security Features

- **PBKDF2 HMAC SHA256**: Passwords are hashed using industry-standard PBKDF2 algorithm
- **Random Salt**: Each password has a unique 32-byte random salt to prevent rainbow table attacks
- **High Iteration Count**: 100,000 iterations provide strong protection against brute force attacks
- **Secure Storage**: Hashed passwords stored in salt:hash format

## Technical Details

- **GUI Framework**: Tkinter
- **Database**: SQLite3 with proper relational schema and foreign key constraints
- **Password Security**: PBKDF2 HMAC SHA256 with random salt and 100,000 iterations
- **Architecture**: MVC-like separation with manager classes
- **Data Persistence**: ACID-compliant transactions with automatic commit/rollback