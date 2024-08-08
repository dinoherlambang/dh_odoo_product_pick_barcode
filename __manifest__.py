# -*- coding: utf-8 -*-
{
    'name': "dh_product_pick_barcode",
    'summary': "Module for picking products using barcodes",
    'description': "Module for picking products using barcodes in stock operations",
    'author': "dinoherlambang",
    'website': "https://www.instagram.com/dinoherlambang/",
    'category': 'Inventory',
    'version': '13.0.1.0.0',
    'depends': ['stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/stock_picking_barcode_views.xml',
        'views/product_variant_views.xml',
        'views/templates.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}