# -*- coding: utf-8 -*-
{
    'name': "Field Translation",
    'summary': """
        Allow Product Fields to Translate Quickly 
    """,
    'description': """
        Allow Product Fields to Translate Quickly 
    """,
    'author': "KP",
    'website': "",
    'images': ['static/description/image.jpg'],
    'category': 'translation',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'product', 'amcl_import_po_extended', 'amcl_import_po'],

    # always loaded
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/translate.xml',
        'wizard/generate_terms_wiz_view.xml',
        'views/menu_item.xml',
    ],
}
