# -*- coding: utf-8 -*-
{
    'name': 'Import - PO',
    'author': 'AMCL',
    'category': 'Extra Tools',
    'summary': 'Purchase Order - Import',
    'description': '''
        Import PO
        ''',
    'version': '15.0.1',
    'depends': ['purchase', 'product', 'stock','amcl_company_branch_ee'],
    'application': True,
    'data': [
        'security/import_po_security.xml',
        'security/ir.model.access.csv',
        'wizard/import_po.xml',
        'wizard/import_message_wizard.xml',
        'wizard/import_inventory.xml',
        'views/product.xml',
        'views/purchase_view.xml',
        'views/stock_picking.xml',
        'views/company_view.xml',
        # 'views/res_config_settings.xml',
        # 'views/menu.xml',
    ],
    'auto_install': True,
    'installable': True,
    'license': 'LGPL-3',
}
