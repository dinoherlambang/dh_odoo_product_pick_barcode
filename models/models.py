from odoo import models, fields, api
from odoo.exceptions import ValidationError
import random

class ProductProduct(models.Model):
    _inherit = 'product.product'

    barcode = fields.Char(string='Barcode', copy=False, index=True)
    qr_code = fields.Char(string='QR Code', copy=False, index=True)

    @api.constrains('barcode')
    def _check_barcode(self):
        for product in self:
            if product.barcode and not product.barcode.isdigit():
                raise ValidationError('Barcode must contain only digits.')

    def action_generate_barcode(self):
        for product in self:
            if not product.barcode:
                product.barcode = ''.join([str(random.randint(0, 9)) for _ in range(13)])

class StockInventory(models.Model):
    _inherit = 'stock.inventory'

    @api.model
    def process_barcode_from_ui(self, inventory_id, barcode, quantity=1):
        inventory = self.browse(inventory_id)
        if inventory.state != 'in_progress':
            return {'success': False, 'message': 'The inventory is not in progress'}

        scan_option = self.env['ir.config_parameter'].sudo().get_param('dh_product_pick_barcode.product_scan_option', 'barcode')
        
        if scan_option == 'barcode':
            product = self.env['product.product'].search([('barcode', '=', barcode)], limit=1)
        elif scan_option == 'qrcode':
            product = self.env['product.product'].search([('qr_code', '=', barcode)], limit=1)
        elif scan_option == 'internal_reference':
            product = self.env['product.product'].search([('default_code', '=', barcode)], limit=1)
        else:  # 'all' option
            product = self.env['product.product'].search(['|', '|',
                ('barcode', '=', barcode),
                ('qr_code', '=', barcode),
                ('default_code', '=', barcode)
            ], limit=1)

        if not product:
            return {'success': False, 'message': 'No product found with this code'}

        line = inventory.line_ids.filtered(lambda l: l.product_id == product)
        if not line:
            line = self.env['stock.inventory.line'].create({
                'product_id': product.id,
                'inventory_id': inventory.id,
                'location_id': inventory.location_id.id,
            })

        line.product_qty += quantity
        return {'success': True, 'message': f'Quantity updated: {product.name} (+{quantity})'}