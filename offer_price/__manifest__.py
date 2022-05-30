# -*- coding: utf-8 -*-
{
    'name': "Price Offer",

    'summary': """
    """,

    'description': """
        
    """,

    'author': "Ibrahim Kaddour",
    'website': "",

    'category': 'Customizations',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['sale_management'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'reports/offer_price.xml',

        'views/sale_order_view.xml',
        'wizard/license_plate_wizard.xml',

    ],
    'qweb': [],
    'demo': [],
}
