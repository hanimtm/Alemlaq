# -*- coding: utf-8 -*-
{
    'name': "Alemlaq Inventory Customisation",

    'summary': """""",

    'description': """
    """,

    'author': "AMCL",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Inventory/Inventory',
    'version': '15.0.1',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['amcl_import_po'],

    # always loaded
    'data': [
        'views/stock_picking_views.xml',
        'security/res_groups.xml',
        'security/security.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
