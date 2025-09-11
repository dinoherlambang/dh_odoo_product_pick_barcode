# How to Use dh_odoo_product_pick_barcode (Odoo 13)

This guide explains how to install, configure, and use the dh_odoo_product_pick_barcode module for barcode-based product picking in Odoo 13 Community Edition.

---

## 1. Installation

1. **Download or Clone the Module**
   - Place the `dh_odoo_product_pick_barcode` folder in your Odoo 13 `addons` directory.

2. **Update App List**
   - Go to Odoo backend: `Apps > Update Apps List`.

3. **Install the Module**
   - Search for `dh_product_pick_barcode` in Apps.
   - Click `Install`.

---


## 2. Configuration

1. **Barcode Field on Products**
   - Go to `Inventory > Products > Product Variants`.
   - Edit a product and set its `Barcode` field.
   - You can use the `Generate Barcode` button to auto-generate a barcode.

2. **User Access Rights**
   - Ensure users have access to Inventory and Picking operations.
   - Check `Settings > Users & Companies > Users` for permissions.

3. **Product Scan Option (New Feature)**
    - Go to `Settings > Inventory`.
    - In the Traceability section, find "Product Scan Option"—styled and grouped like other Odoo settings.
    - Choose how barcode scanning updates product quantity:
       - **Auto Increment (each scan adds 1):** Each scan increases quantity by 1 automatically.
       - **Manual Entry (use quantity field):** Manually enter the quantity before scanning, for bulk or custom updates.
    - Save your settings. The module will use your selected option for all barcode picking and inventory operations.

---

## 3. Using Barcode Picking


### A. Picking Products with Barcode

1. Go to `Inventory > Operations > Transfers`.
2. Open a picking (delivery or receipt).
3. In the picking form, you will see a `Scan products` section (if picking is not done/cancelled).
4. Use a barcode scanner or manually enter the barcode in the input field.
5. Depending on your scan option:
   - **Auto Increment:** Just scan the barcode; each scan adds 1 to the quantity automatically.
   - **Manual Entry:** Enter the desired quantity in the quantity field before scanning, then scan the barcode.
6. Click `Add` if needed.
7. The system will:
   - Match the barcode to a product.
   - Update the picked quantity.
   - Show success or error messages (wrong product, excess quantity, product not found).


### B. Inventory Adjustments with Barcode

1. Go to `Inventory > Operations > Inventory Adjustments`.
2. Open an inventory in progress.
3. In the form, you will see a `Scan products` section.
4. Depending on your scan option:
   - **Auto Increment:** Just scan the barcode; each scan adds 1 to the quantity automatically.
   - **Manual Entry:** Enter the desired quantity in the quantity field before scanning, then scan the barcode.
5. Click `Add` if needed.
6. The system will update the inventory line for the scanned product.

---

## 4. Tips & Troubleshooting

- **Barcode Not Found:**
  - Ensure the product has a barcode set.
  - Check for typos or incorrect barcode format.

- **Excess Quantity Warning:**
  - The module prevents picking more than planned. Adjust planned quantity if needed.

- **Product Not in Picking/Inventory:**
  - Only products in the original picking/inventory can be updated by scanning.

- **Supported Devices:**
  - Works with USB barcode scanners or manual entry in browser.
  - For mobile or advanced hardware, further customization may be needed.

---

## 5. Advanced Usage & Customization

- You can extend the module to support lot/serial numbers, mobile optimization, or additional scan options.
- For technical customization, see the Python and JS files in the module.

---

## 6. Support

For issues or feature requests, contact the author:
- Instagram: [@dinoherlambang](https://www.instagram.com/dinoherlambang/)

---

Enjoy barcode-based picking in Odoo 13 Community!
