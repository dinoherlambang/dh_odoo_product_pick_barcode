from odoo import models, fields, api
from odoo.exceptions import ValidationError
import random

class ProductProduct(models.Model):
    _inherit = 'product.product'

    ean13 = fields.Char(string='EAN-13 Barcode', copy=False, index=True)

    @api.constrains('ean13')
    def _check_ean13(self):
        for product in self:
            if product.ean13 and not product.ean13.isdigit():
                raise ValidationError('EAN-13 Barcode must contain only digits.')

    def action_generate_ean13(self):
        for product in self:
            if not product.ean13:
                product.ean13 = ''.join([str(random.randint(0, 9)) for _ in range(13)])

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.model
    def process_barcode_from_ui(self, picking_id, barcode, quantity=1):
        picking = self.browse(picking_id)
        if picking.state == 'done':
            return {'success': False, 'message': 'The picking is already validated'}

        product = self.env['product.product'].search([('ean13', '=', barcode)], limit=1)
        if not product:
            return {'success': False, 'message': 'No product found with this barcode'}

        move_line = picking.move_line_ids.filtered(lambda l: l.product_id == product)
        if not move_line:
            # Create a new move line if the product is not in the picking
            move_line = self.env['stock.move.line'].create({
                'product_id': product.id,
                'product_uom_id': product.uom_id.id,
                'picking_id': picking.id,
                'location_id': picking.location_id.id,
                'location_dest_id': picking.location_dest_id.id,
            })

        move_line.qty_done += quantity
        return {'success': True, 'message': f'Quantity updated: {product.name} (+{quantity})'}

class StockInventory(models.Model):
    _inherit = 'stock.inventory'

    @api.model
    def process_barcode_from_ui(self, inventory_id, barcode, quantity=1):
        inventory = self.browse(inventory_id)
        if inventory.state != 'in_progress':
            return {'success': False, 'message': 'The inventory is not in progress'}

        product = self.env['product.product'].search([('ean13', '=', barcode)], limit=1)
        if not product:
            return {'success': False, 'message': 'No product found with this barcode'}

        line = inventory.line_ids.filtered(lambda l: l.product_id == product)
        if not line:
            line = self.env['stock.inventory.line'].create({
                'product_id': product.id,
                'inventory_id': inventory.id,
                'location_id': inventory.location_id.id,
            })

        line.product_qty += quantity
        return {'success': True, 'message': f'Quantity updated: {product.name} (+{quantity})'}