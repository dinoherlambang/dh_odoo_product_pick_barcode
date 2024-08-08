# -*- coding: utf-8 -*-
# from odoo import http


# class DhProductPickBarcode(http.Controller):
#     @http.route('/dh_product_pick_barcode/dh_product_pick_barcode/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dh_product_pick_barcode/dh_product_pick_barcode/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('dh_product_pick_barcode.listing', {
#             'root': '/dh_product_pick_barcode/dh_product_pick_barcode',
#             'objects': http.request.env['dh_product_pick_barcode.dh_product_pick_barcode'].search([]),
#         })

#     @http.route('/dh_product_pick_barcode/dh_product_pick_barcode/objects/<model("dh_product_pick_barcode.dh_product_pick_barcode"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dh_product_pick_barcode.object', {
#             'object': obj
#         })
