from odoo import models, api, _
from odoo.exceptions import UserError

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.model
    def process_barcode_from_ui(self, picking_id, barcode, quantity=1):
        picking = self.browse(picking_id)
        if picking.state == 'done':
            return {'success': False, 'message': _('The picking is already validated')}

        scan_option = self.env['ir.config_parameter'].sudo().get_param('dh_product_pick_barcode.product_scan_option', 'barcode')
        
        if scan_option == 'barcode':
            product = self.env['product.product'].search([('ean13', '=', barcode)], limit=1)
        elif scan_option == 'qrcode':
            product = self.env['product.product'].search([('qr_code', '=', barcode)], limit=1)  # Assuming you have a qr_code field
        elif scan_option == 'internal_reference':
            product = self.env['product.product'].search([('default_code', '=', barcode)], limit=1)
        else:  # 'all' option
            product = self.env['product.product'].search(['|', '|',
                ('ean13', '=', barcode),
                ('qr_code', '=', barcode),
                ('default_code', '=', barcode)
            ], limit=1)

        if not product:
            return {'success': False, 'message': _('No product found with this code')}

        move_line = picking.move_line_ids.filtered(lambda l: l.product_id == product)
        if not move_line:
            return {
                'success': False,
                'message': _('Product %s is not in the current picking. Do you want to add it?') % product.name,
                'product_not_in_picking': True,
                'product_id': product.id,
                'product_name': product.name
            }

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

    @api.model
    def add_product_to_picking(self, picking_id, product_id, quantity):
        picking = self.browse(picking_id)
        product = self.env['product.product'].browse(product_id)

        move = self.env['stock.move'].create({
            'name': product.name,
            'product_id': product.id,
            'product_uom_qty': quantity,
            'product_uom': product.uom_id.id,
            'picking_id': picking.id,
            'location_id': picking.location_id.id,
            'location_dest_id': picking.location_dest_id.id,
        })
        move._action_confirm()
        move._action_assign()

        return True