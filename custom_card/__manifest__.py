# -*- coding: utf-8 -*-
{
    'name': "Custom Card Request",

    'summary': """""",

    'description': """
    """,

    'author': "AMCL",

    # for the full list
    'category': 'Sale',
    'version': '15.0.1',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['sale','sale_management'],

    # always loaded
    'data': [
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'data/custom_card_request_sequence.xml',
        'views/custom_card_request_views.xml',
        'views/sale_order_views.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'images': [
    ],
}
