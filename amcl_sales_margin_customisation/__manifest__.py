# -*- coding: utf-8 -*-

{
    'name': 'Alemlaq Sale Margin Customisation',
    'author': 'AMCL',
    'category': 'Sales',
    'summary': 'Alemlaq Sale Margin Customisation',
    'description': '''
        Alemlaq Sale Margin Customisation
                    ''',
    'version': '15.0.1',
    'depends': ['sale_management','sales_team'],
    'application': True,
    'data': [
            'views/globalmargin.xml',
            'views/product.xml',
            'security/ir.model.access.csv',
            'data/data.xml',
    ],
    'license': 'LGPL-3',
    'auto_install': False,
    'installable': True,

}
