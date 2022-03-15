# -*- coding: utf-8 -*-
{
    'name': "Al-Emlak",

    'summary': """Printed Report Template Al Emlak Trading""",

    'description': """
    """,

    'author': "Ibrahim Kaddour",
    'website': "",

    'category': 'Customizations',
    'version': '15.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'sale_management', 'contacts'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/amcl_sale_order_inherit.xml',
        'views/amcl_payment_inherit.xml',

        'reports/ordinary_confession_report.xml',
        'reports/receipt_form_report.xml',
        'reports/form_nb_4_report.xml',
        'reports/user_acknowledgment_form_report.xml',
        'reports/catch_receipt_report.xml',
        'reports/vehicle_registration_woman_report.xml',
        'reports/vehicle_registration_agency_report.xml',
        'reports/vehicle_registration_authorization_report.xml',

        'wizard/views/amcl_report_wizard.xml'

    ],
    'qweb': [],
    # only loaded in demonstration mode
    'demo': [],
}
