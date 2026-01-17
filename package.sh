#!/bin/bash

# Package Inventory Manager Desktop App
# Creates a distributable archive with all necessary files

echo "=== Packaging Inventory Manager Desktop App ==="
echo ""

# Check if executable exists
if [ ! -f "dist/InventoryManager" ]; then
    echo "Error: Executable not found. Please build the app first with PyInstaller."
    exit 1
fi

# Create package directory
PACKAGE_NAME="InventoryManager_v1.0_Linux"
PACKAGE_DIR="dist/$PACKAGE_NAME"
echo "Creating package directory: $PACKAGE_DIR"

mkdir -p "$PACKAGE_DIR"

# Copy files
echo "Copying application files..."
cp "dist/InventoryManager" "$PACKAGE_DIR/"
cp "inventory.db" "$PACKAGE_DIR/"
cp "install.sh" "$PACKAGE_DIR/"
cp "DESKTOP_APP_README.md" "$PACKAGE_DIR/README.md"

# Create archive
echo "Creating distribution archive..."
cd dist
tar -czf "${PACKAGE_NAME}.tar.gz" "$PACKAGE_NAME"

echo ""
echo "✅ Packaging completed successfully!"
echo ""
echo "Distribution package created:"
echo "📦 dist/${PACKAGE_NAME}.tar.gz"
echo ""
echo "Package contents:"
echo "├── InventoryManager           # Standalone executable"
echo "├── inventory.db              # SQLite database"
echo "├── install.sh                # Installation script"
echo "└── README.md                 # User documentation"
echo ""
echo "To distribute:"
echo "1. Share the .tar.gz file"
echo "2. Users extract and run: ./install.sh"
echo "3. Application appears in their desktop menu"
echo ""
echo "Archive size: $(ls -lh "${PACKAGE_NAME}.tar.gz" | awk '{print $5}')"