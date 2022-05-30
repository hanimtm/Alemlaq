# -*- coding: utf-8 -*-
{
    'name': "Sale Order Attach Ext",

    'summary': """""",

    'description': """
    """,

    'author': "Ibrahim",

    # for the full list
    'category': 'Sale',
    'version': '15.0.1',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['sale', 'sale_management', 'amcl_sales_customisation'],

    # always loaded
    'data': [
        'views/res_partner.xml',
        'views/sale_order_views.xml',
        'views/account_move.xml',
        'reports/rajhi_report.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'images': [
    ],
}
