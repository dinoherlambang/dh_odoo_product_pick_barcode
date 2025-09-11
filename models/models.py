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
            return {'success': False, 'message': _('The inventory is not in progress')}

        product = self._find_product_by_scan_option(barcode)

        if not product:
            return {'success': False, 'message': _('No product found with this code')}

        line = inventory.line_ids.filtered(lambda l: l.product_id == product)
        if not line:
            return {'success': False, 'message': _('Product not in the original inventory. Cannot be added.')}

        line.product_qty += quantity


# Add product_scan_option to res.config.settings
from odoo import models, fields, api, _

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    product_scan_option = fields.Selection([
        ('auto', 'Auto Increment (each scan adds 1)'),
        ('manual', 'Manual Entry (use quantity field)'),
    ],
        string='Product Scan Option',
        default='auto',
        help='Choose how barcode scanning updates product quantity in picking/inventory.')

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('dh_odoo_product_pick_barcode.product_scan_option', self.product_scan_option)

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        option = self.env['ir.config_parameter'].sudo().get_param('dh_odoo_product_pick_barcode.product_scan_option', default='auto')
        res.update(product_scan_option=option)
        return res
        return {'success': True, 'message': _('Quantity updated: %s (+%s)') % (product.name, quantity)}