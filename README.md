# Product Pick Barcode

## Overview
The Product Pick Barcode module enhances Odoo's stock management capabilities by adding barcode scanning functionality to stock picking and inventory adjustment processes. This module streamlines warehouse operations, improves accuracy, and increases efficiency in inventory management.

## Key Features
- Multi-format product identification: Support for barcodes, QR codes, and internal references
- Integrated barcode scanning interface for stock picking, incoming shipments, and inventory adjustment forms
- Real-time quantity updates: Immediately updates product quantities in the current operation when scanned
- User-friendly notifications for successful scans and errors
- Configurable product scan options: Barcode, QR Code, Internal Reference, or All
- Incoming shipment support: Scan products and serial numbers for efficient receipt processing
- Serial number assignment: Assigns serial numbers to products during incoming shipments
- Inventory adjustment: Barcode scanning functionality for streamlined inventory counts
- Improved error handling: Enhanced messages for various scenarios during scanning
- Mobile-friendly interface: Optimized for use with handheld scanners
- Flexible product identification: Choose between barcode, QR code, internal reference, or all methods

## Installation
1. Place the `dh_product_pick_barcode` folder in your Odoo addons directory.
2. Update the addons list in your Odoo instance.
3. Install the module through the Odoo Apps menu.

## Configuration
1. Go to Inventory > Configuration > Settings.
2. Locate the "Product Scan Option" section.
3. Choose the preferred scan option: Barcode, QR Code, Internal Reference, or All.
4. Save the configuration.

## Usage
### Stock Picking (Outgoing Shipments)
1. Open a stock picking form (e.g., delivery order or internal transfer).
2. Locate the "Scan products" section at the bottom of the form.
3. Use a barcode scanner to scan product barcodes, QR codes, or internal references (based on configuration).
4. Optionally, enter a quantity before scanning if adding multiple units.
5. The system automatically updates quantities or adds new lines as needed.
6. Complete the picking process as usual.

### Incoming Shipments
1. Open an incoming shipment form.
2. Find the "Scan products and serial numbers" section.
3. Scan product barcodes or serial numbers.
4. The system will automatically update quantities and assign serial numbers.
5. Complete the receipt process as normal.

### Inventory Adjustment
1. Start a new inventory adjustment.
2. Use the barcode scanner to count products (using the configured scan option).
3. The system automatically updates product quantities in the inventory.
4. Validate the inventory when counting is complete.

## Technical Details
- Extends `product.product`, `stock.picking`, and `stock.inventory` models
- Custom JavaScript for capturing barcode scan events and communicating with the server
- Compatible with Odoo 13.0 Community Edition

### Barcode Processing Logic
The `process_barcode_from_ui` method in the `StockPicking` model handles the core barcode scanning functionality:

1. Checks if the picking is already validated.
2. Finds the product using the scanned code based on the configured scan option.
3. Handles cases for products not found, unexpected products, or products not in the picking.
4. Updates quantities or creates new move lines as needed.
5. Manages excess quantities and provides appropriate feedback.

For incoming shipments, the `process_barcode_from_ui_incoming` method provides additional functionality:

1. Supports scanning of both product barcodes and serial numbers.
2. Automatically assigns serial numbers to products.
3. Creates new move lines for products not in the original receipt.

These methods ensure accurate and efficient processing of scanned products during various stock operations, with flexibility in product identification methods and robust error handling.

## Error Handling
The module includes comprehensive error handling for various scenarios:
- Invalid barcodes
- Products not found in the system
- Products not in the current picking
- Excess quantities
- Unexpected products in the picking

Each error case provides a specific message to guide the user in resolving the issue.

## Dependencies
- `stock` module

## Author
dinoherlambang

## Version
13.0.1.0.0

## License
LGPL-3

## Support
For support, feature requests, or bug reports, please contact the author or create an issue in the module's repository.