from odoo import models, api, _
from odoo.exceptions import UserError

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.model
    def process_barcode_from_ui(self, picking_id, barcode, quantity=1):
        picking = self.browse(picking_id)
        if picking.state == 'done':
            return {'success': False, 'message': _('The picking is already validated')}

        product = self.env['product.product'].search([('ean13', '=', barcode)], limit=1)
        if not product:
            return {'success': False, 'message': _('No product found with this barcode')}

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

        new_qty_done = move_line.qty_done + quantity
        initial_demand = move_line.move_id.product_uom_qty

        if new_qty_done > initial_demand:
            return {
                'success': False,
                'message': _('Warning: The scanned quantity (%s) exceeds the initial demand (%s) for %s') % (new_qty_done, initial_demand, product.name),
                'excess': True
            }

        move_line.qty_done = new_qty_done
        return {'success': True, 'message': _('Quantity updated: %s (+%s)') % (product.name, quantity)}

    @api.model
    def force_update_quantity(self, picking_id, barcode, quantity):
        picking = self.browse(picking_id)
        product = self.env['product.product'].search([('ean13', '=', barcode)], limit=1)
        move_line = picking.move_line_ids.filtered(lambda l: l.product_id == product)
        
        if move_line:
            move_line.qty_done += quantity
        else:
            self.env['stock.move.line'].create({
                'product_id': product.id,
                'product_uom_id': product.uom_id.id,
                'picking_id': picking.id,
                'location_id': picking.location_id.id,
                'location_dest_id': picking.location_dest_id.id,
                'qty_done': quantity,
            })

        return True