from odoo import models, api, _
from odoo.exceptions import UserError

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.model
    def process_barcode_from_ui(self, picking_id, barcode, quantity=1):
        picking = self.browse(picking_id)
        if picking.state == 'done':
            return {'success': False, 'message': _('The picking is already validated')}

        product = self._find_product_by_scan_option(barcode)

        if not product:
            return {
                'success': False,
                'message': _('No product found with this code. Please check the barcode and try again.'),
                'no_product_found': True
            }

        expected_move_lines = picking.move_line_ids.filtered(lambda l: l.product_id != product and l.qty_done < l.product_uom_qty)
        if expected_move_lines:
            expected_products = ', '.join(expected_move_lines.mapped('product_id.name'))
            return {
                'success': False,
                'message': _('Warning: Scanned product (%s) is different from expected products (%s)') % (product.name, expected_products),
                'unexpected_product': True,
                'scanned_product_id': product.id
            }

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
                'message': _('Product not in the original picking. Cannot be added.'),
                'product_not_in_picking': True
            }


    @api.model
    def process_barcode_from_ui_incoming(self, picking_id, barcode, quantity=1):
        picking = self.browse(picking_id)
        if picking.state == 'done':
            return {'success': False, 'message': _('The picking is already validated')}

        product = self._find_product_by_scan_option(barcode)

        if not product:
            # Check if the scanned barcode is a serial number
            lot = self.env['stock.production.lot'].search([('name', '=', barcode)], limit=1)
            if lot:
                product = lot.product_id
            else:
                return {
                    'success': False,
                    'message': _('No product or serial number found with this code. Please check the barcode and try again.'),
                    'no_product_found': True
                }

        move_line = picking.move_line_ids.filtered(lambda l: l.product_id == product)
        if move_line:
            if lot:
                if move_line.lot_id:
                    return {'success': False, 'message': _('Serial number already set for this product')}
                move_line.lot_id = lot.id
            move_line.qty_done += quantity
            return {'success': True, 'message': _('Quantity updated for %s') % product.name}
        else:
            new_move_line = self.env['stock.move.line'].create({
                'product_id': product.id,
                'product_uom_id': product.uom_id.id,
                'picking_id': picking.id,
                'location_id': picking.location_id.id,
                'location_dest_id': picking.location_dest_id.id,
                'qty_done': quantity,
                'lot_id': lot.id if lot else False,
            })
            return {'success': True, 'message': _('Product added: %s') % product.name}

    def _find_product_by_scan_option(self, barcode):
        scan_option = self.env['ir.config_parameter'].sudo().get_param('dh_product_pick_barcode.product_scan_option', 'barcode')
        if scan_option == 'barcode':
            return self.env['product.product'].search([('barcode', '=', barcode)], limit=1)
        elif scan_option == 'qrcode':
            return self.env['product.product'].search([('qr_code', '=', barcode)], limit=1)
        elif scan_option == 'internal_reference':
            return self.env['product.product'].search([('default_code', '=', barcode)], limit=1)
        else:  # 'all' option
            return self.env['product.product'].search(['|', '|',
                ('barcode', '=', barcode),
                ('qr_code', '=', barcode),
                ('default_code', '=', barcode)
            ], limit=1)

    @api.model
    def force_update_quantity(self, picking_id, barcode, quantity):
        picking = self.browse(picking_id)
        product = self._find_product_by_scan_option(barcode)
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
