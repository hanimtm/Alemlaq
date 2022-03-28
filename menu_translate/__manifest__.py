# -*- coding: utf-8 -*-
{
    'name': "Translation",

    'summary': """
    """,

    'description': """
        
    """,

    'author': "Ibrahim Kaddour",
    'website': "",
    'images': ['static/description/image.jpg'],
    'category': 'Customizations',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['stock'],

    # always loaded
    'data': [
        'security/groups.xml',
        'views/translate.xml',
        'views/menu_item.xml',
    ],
    'qweb': [],
    'demo': [],
}
