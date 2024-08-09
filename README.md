# Product Pick Barcode

## Overview
The Product Pick Barcode module enhances Odoo's stock management capabilities by adding barcode scanning functionality to stock picking and inventory adjustment processes. This module streamlines warehouse operations, improves accuracy, and increases efficiency in inventory management.

## Key Features
- EAN-13 barcode support for products
- Barcode scanning interface integrated into stock picking and inventory adjustment forms
- Real-time product quantity updates based on scanned barcodes
- Automatic creation of move lines for scanned products not in the original picking
- Multiple quantity input for batch scanning
- User-friendly notifications for successful scans and errors

## Additional Features
- Inventory adjustment: Barcode scanning functionality for inventory counts
- Improved error handling: Enhanced messages for invalid barcodes or products not in the current operation
- Mobile-friendly interface: Optimized for use with handheld scanners

## Installation
1. Place the `dh_product_pick_barcode` folder in your Odoo addons directory.
2. Update the addons list in your Odoo instance.
3. Install the module through the Odoo Apps menu.

## Configuration
No additional configuration is required. The module automatically adds barcode scanning functionality to stock picking and inventory adjustment operations.

## Usage
### Stock Picking
1. Open a stock picking form (e.g., delivery order or internal transfer).
2. Locate the "Scan products" section at the bottom of the form.
3. Use a barcode scanner to scan product barcodes.
4. Optionally, enter a quantity before scanning if adding multiple units.
5. The system automatically updates quantities or adds new lines as needed.
6. Complete the picking process as usual.

### Inventory Adjustment
1. Start a new inventory adjustment.
2. Use the barcode scanner to count products.
3. The system automatically updates product quantities in the inventory.
4. Validate the inventory when counting is complete.

## Technical Details
- Extends `product.product`, `stock.picking`, and `stock.inventory` models
- Custom JavaScript for capturing barcode scan events and communicating with the server
- Compatible with Odoo 13.0 Community Edition

### Barcode Processing Logic
The `process_barcode_from_ui` method in the `StockPicking` model handles the core barcode scanning functionality:

1. Checks if the picking is already validated.
2. Searches for the product using the scanned barcode.
3. Finds or creates a move line for the product.
4. Checks if the new quantity exceeds the initial demand.
5. Updates the quantity if it doesn't exceed the initial demand.

This logic ensures accurate and efficient processing of scanned products during stock operations.

## Dependencies
- `stock` module

## Author
dinoherlambang

## Version
13.0.1.0.0

## License
LGPL-3