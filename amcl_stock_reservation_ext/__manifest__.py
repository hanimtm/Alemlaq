# -*- coding: utf-8 -*-

{
    'name': 'Stock Reservation on Sales Flow - Extension',
    'version': '1.0.1',
    'category': 'Inventory/Inventory',
    'license': 'Other proprietary',
    'summary': """This app allow you to manage stock reservation from your Quote/Sales.""",
    'description': """
    """,
    'author': 'Aneesh.AV',
    'depends': [
        'odoo_stock_reservation'
    ],
    'data': [
        'views/sale_order_view.xml',
    ],
    'installable': True,
    'application': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
