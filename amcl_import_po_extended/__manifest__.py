# -*- coding: utf-8 -*-

{
    'name': 'Amcl Import Po Extended',
    'author': 'AMCL',
    'category': 'Purchase',
    'summary': 'Purchase Order - Import',
    'description': '''
        Import PO
                    ''',
    'version': '15.0.1',
    'depends': ['amcl_import_po'],
    'application': True,
    'data': [
        'views/purchase_view.xml',
        'views/product.xml',
        'views/stock_picking.xml'
    ],
    'auto_install': True,
    'installable': True,
    'license': 'LGPL-3',
}
