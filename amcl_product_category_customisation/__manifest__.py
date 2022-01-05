# -*- coding: utf-8 -*-

{
    'name': 'Alemlaq Product Category Customisation',
    'author': 'AMCL',
    'category': 'Sales',
    'summary': 'Product Category Customisation',
    'description': '''
        Product Category Customisation
                    ''',
    'version': '15.0.1',
    'depends': ['sale_management', 'product'],
    'application': True,
    'data': [
        'security/security.xml',
        'views/product_category_views.xml',
    ],
    'license': 'LGPL-3',
    'auto_install': False,
    'installable': True,

}