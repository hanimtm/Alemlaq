# -*- coding: utf-8 -*-
{
    'name': "Tracking Report",

    'summary': """
    """,

    'description': """
        
    """,

    'author': "Ibrahim Kaddour",
    'website': "",
    'images': ['static/description/img.png'],
    'category': 'Customizations',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['stock', 'amcl_import_po'],

    # always loaded
    'data': [
        'security/groups.xml',
        'views/pivot_table.xml',
        'views/menu_item.xml',

    ],
    'qweb': [],
    'demo': [],
}
