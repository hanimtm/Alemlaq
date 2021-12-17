# -*- coding: utf-8 -*-
{
    'name': 'Saudi Invoice Format',
    'version': '1.0',
    'depends': ['base', 'account'],
    'category': 'Accounting',
    'author': 'AMCL',
    'data': [
        'views/res_company.xml',
        'views/invoice.xml',
        'views/res_partner.xml',
        'reports/report_saudi_invoice.xml',
     ],
    'assets': {
        'web.report_assets_pdf': [
            'saudi_vat_invoice_print/static/**/*',
        ],
        'web.assets_qweb': [
            'saudi_vat_invoice_print/static/src/xml/**/*',
        ],
    },
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
}
