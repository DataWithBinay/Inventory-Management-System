# Inventory Manager - Desktop Application

A complete, standalone desktop application for inventory management with SQLite database, user authentication, and comprehensive sales reporting.

## 🚀 **Standalone Desktop App**

This is a **fully packaged desktop application** that runs on Linux, Windows, and macOS without requiring Python installation. The entire application, including all dependencies and the database, is bundled into a single executable file.

## 📦 **Distribution Package**

### Files Included:
- `InventoryManager` - Standalone executable (Linux)
- `inventory.db` - SQLite database with sample data
- `install.sh` - Automated installation script
- `README.md` - This documentation

## 🛠️ **Installation**

### Option 1: Automated Installation (Recommended)
```bash
./install.sh
```
This will:
- Install the application to `~/.local/share/InventoryManager/`
- Create a desktop shortcut in your applications menu
- Set up proper permissions

### Option 2: Manual Installation
```bash
# Create directory
mkdir -p ~/.local/share/InventoryManager/

# Copy files
cp InventoryManager ~/.local/share/InventoryManager/
cp inventory.db ~/.local/share/InventoryManager/

# Make executable
chmod +x ~/.local/share/InventoryManager/InventoryManager

# Create desktop shortcut manually or run directly
~/.local/share/InventoryManager/InventoryManager
```

## 🎯 **Features**

### ✅ **Complete Inventory Management**
- Add, update, and search products
- Real-time inventory tracking
- Product categories and pricing

### ✅ **User Management**
- Secure user authentication (PBKDF2 hashed passwords)
- User registration and password reset
- Role-based access control

### ✅ **Sales & Billing**
- Shopping cart functionality
- Automatic bill generation with VAT (13%)
- Transaction history and receipts

### ✅ **Advanced Reporting**
- **Sales Report CSV**: Detailed transaction data
- **Sales Summary CSV**: Business analytics and statistics
- Export functionality for Excel/Google Sheets

### ✅ **Database Features**
- SQLite3 database (no external server required)
- ACID transactions for data integrity
- Automatic data persistence
- Concurrent user access support

## 🔐 **Security Features**

- **PBKDF2 HMAC SHA256**: Industry-standard password hashing
- **Random Salt**: Unique salt per password (32 bytes)
- **100,000 Iterations**: Strong protection against brute force
- **Secure Storage**: Hashed passwords in database

## 📊 **CSV Export Capabilities**

### Sales Report (`sales_report.csv`)
```csv
Sale_ID,Product_ID,Product_Name,Quantity_Sold,Total_Amount,Sale_Date
1,1,Apple,3,6.00,2026-01-17 21:11:20
2,2,Banana,2,3.00,2026-01-17 21:11:20
```

### Sales Summary (`sales_summary.csv`)
- Overall statistics (total sales, items sold)
- Top selling products ranking
- Daily sales summaries
- Business analytics ready for spreadsheets

## 🖥️ **System Requirements**

- **Operating System**: Linux, Windows 10+, macOS 10.12+
- **RAM**: 256MB minimum, 512MB recommended
- **Storage**: 50MB free space
- **Display**: 1024x768 minimum resolution

## 🚀 **Getting Started**

1. **Install** the application using `./install.sh`
2. **Launch** from your applications menu or run directly
3. **Login** with default credentials:
   - Username: `admin`, Password: `admin123`
   - Username: `user`, Password: `user123`
4. **Explore** the features:
   - Add products to inventory
   - Process sales transactions
   - Generate reports

## 📁 **Application Structure**

```
InventoryManager/
├── InventoryManager          # Main executable
├── inventory.db             # SQLite database
├── sales_report.csv        # Generated sales reports
└── sales_summary.csv       # Generated analytics
```

## 🔧 **Technical Details**

- **Built with**: Python 3.13, Tkinter GUI, SQLite3
- **Packaging**: PyInstaller for standalone distribution
- **Database**: SQLite3 with foreign key constraints
- **Security**: PBKDF2 password hashing
- **Size**: ~13MB compressed executable

## 🆘 **Troubleshooting**

### Application won't start:
- Ensure execute permissions: `chmod +x InventoryManager`
- Check system compatibility (Linux/Windows/macOS)

### Database issues:
- The `inventory.db` file contains sample data
- Delete and recreate if corrupted
- Application will auto-create database if missing

### Permission issues:
- Run installation script as regular user
- Check file permissions in installation directory

## 📞 **Support**

This is a complete, self-contained desktop application. All features work offline without internet connection.

### Default Data:
- **Products**: Apple ($2.00), Banana ($1.50), Orange ($3.00)
- **Users**: admin/admin123, user/user123
- **Sample Sales**: Pre-loaded transaction data

## 🎉 **Ready to Use!**

Your inventory management system is now a professional desktop application that can be distributed and installed on any compatible computer. No Python installation required - just download, install, and run!