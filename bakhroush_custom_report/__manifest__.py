# -*- coding: utf-8 -*-

{
    # Module Information
    'name': 'Bakhroush Custom - Report',
    'category': 'Fleet Custom',
    'sequence': 1,
    'version': '15.0.1.0.0',
    'license': 'LGPL-3',
    'summary': """Bakhroush Custom - Report""",
    'description': """Bakhroush Custom - Report""",
    # Website
    'author': 'AMCL',
    # Dependencies
    'depends': ['base', 'product', 'stock', 'amcl_saudi_vat_invoice_print', 'sale', 'amcl_company_branch_ee',
                'purchase', 'contacts'],
    # Data
    'data': [
        'views/data.xml',
        'security/ir.model.access.csv',
        'report/delivery_report.xml',
        'report/delivery_dotmatrix_report.xml',
        'report/delivery_concreate_dotmatrix_report.xml',
        'views/stock_picking_view.xml',
        'views/sale_view.xml',
        'views/purchase_view.xml',
        # 'views/mrp.xml',
        'views/res_partner_view.xml',
        'views/product_view.xml',
        'views/payment_terms.xml',
        'views/branch.xml'
         ],
    'installable': True,
    'application': True,
}