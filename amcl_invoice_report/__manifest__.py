 # -*- coding: utf-8 -*-
{
    'name': "Invoice Report Customization",
    'summary': """
        Invoice Report Customization
        """,
    'description': """
        Invoice Report Changes As per the Company Policy.
        """,
    'author': "AMCL",
    'category': 'account',
    'version': '15.0.1.0',
    'depends': ['account'],
    'data': [
        'reports/invoice_report_template_view.xml',
        'reports/invoice_report_view.xml',
        'views/account_move.xml',
    ],
    'license': 'LGPL-3',
    'auto_install': False,
    'installable': True,
}