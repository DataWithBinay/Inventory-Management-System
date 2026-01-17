#!/bin/bash

# Inventory Manager Desktop App Installer
# This script installs the Inventory Manager desktop application

echo "=== Inventory Manager Desktop App Installer ==="
echo ""

# Check if we're in the right directory
if [ ! -f "dist/InventoryManager" ]; then
    echo "Error: Executable not found. Please run this script from the project directory."
    exit 1
fi

# Create installation directory
INSTALL_DIR="$HOME/.local/share/InventoryManager"
echo "Creating installation directory: $INSTALL_DIR"
mkdir -p "$INSTALL_DIR"

# Copy executable and database
echo "Copying application files..."
cp "dist/InventoryManager" "$INSTALL_DIR/"
cp "inventory.db" "$INSTALL_DIR/"

# Create desktop entry
DESKTOP_FILE="$HOME/.local/share/applications/inventory-manager.desktop"
echo "Creating desktop shortcut..."
cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Inventory Manager
Comment=Complete inventory management system
Exec=$INSTALL_DIR/InventoryManager
Icon=package
Terminal=false
Categories=Office;Utility;
EOF

# Make executable
chmod +x "$INSTALL_DIR/InventoryManager"

echo ""
echo "✅ Installation completed successfully!"
echo ""
echo "You can now:"
echo "1. Launch from Applications menu: 'Inventory Manager'"
echo "2. Or run directly: $INSTALL_DIR/InventoryManager"
echo ""
echo "The application includes:"
echo "- Complete inventory management system"
echo "- SQLite database with sample data"
echo "- User authentication and registration"
echo "- Sales tracking and reporting"
echo "- CSV export functionality"
echo ""
echo "Default login credentials:"
echo "- Username: admin, Password: admin123"
echo "- Username: user, Password: user123"