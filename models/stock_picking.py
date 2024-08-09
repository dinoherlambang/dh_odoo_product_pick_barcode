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
            return {'success': False, 'message': _('No product found with this code')}

        move_line = picking.move_line_ids.filtered(lambda l: l.product_id == product)
        if move_line:
            if move_line.qty_done + quantity > move_line.product_uom_qty:
                return {
                    'success': False,
                    'message': _('Scanned quantity exceeds the planned quantity.'),
                    'excess': True
                }
            move_line.qty_done += quantity
            return {'success': True, 'message': _('Quantity updated for %s') % product.name}
        else:
            return {
                'success': False,
                'message': _('Product not in the picking. Do you want to add it?'),
                'product_not_in_picking': True,
                'product_id': product.id
            }

    @api.model
    def force_update_quantity(self, picking_id, barcode, quantity):
        picking = self.browse(picking_id)
        product = self.env['product.product'].search([('barcode', '=', barcode)], limit=1)
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