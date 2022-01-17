# -*- coding: utf-8 -*-

{
    'name': 'Material Purchase Requisitions by Employees/Users',
    'version': '13.0.1',
    'summary': """This module allow your employees/users to create Purchase Requisitions.""",
    'description': """
    Material Purchase Requisitions
    """,
    'author': 'Aneesh.AV',
    'category': 'Warehouse',
    'depends': [
                'stock',
                'hr',
                'purchase',
                ],
    'data':[
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/purchase_requisition_sequence.xml',
        'data/employee_purchase_approval_template.xml',
        'data/confirm_template_material_purchase.xml',
        'report/purchase_requisition_report.xml',
        'views/purchase_requisition_view.xml',
        'views/hr_employee_view.xml',
        'views/hr_department_view.xml',
        'views/stock_picking_view.xml',
    ],
    'installable' : True,
    'application' : False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
