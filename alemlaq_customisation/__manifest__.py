# -*- coding: utf-8 -*-
{
    'name': "Alemlaq Customisation",

    'summary': """""",

    'description': """
    """,

    'author': "AMCL",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '15.0.1',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['account'],

    # always loaded
    'data': [
        'views/res_partner_views.xml',
        'views/account_move_view.xml',
        'views/stock_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'images': [
        'static/description/banner.PNG',
        'static/description/icon.PNG',
        'static/description/image1.PNG',
        'static/description/image2.PNG',
        'static/description/image3.PNG',
        'static/description/image4.PNG',
    ],
}
