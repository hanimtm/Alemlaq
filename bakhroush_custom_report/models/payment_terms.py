# -*- coding: utf-8 -*-

from odoo import fields, models , api, _
from odoo.exceptions import ValidationError


class PaymentTerms(models.Model):
    _inherit = 'account.payment.term'

    allowed_users = fields.Many2many('res.users', string='Allowed Users')
    force_invoice = fields.Boolean('Create auto Invoice & Payment')
    default_cash_payment = fields.Many2one('account.journal', 'Payment Journal')
    payment_type = fields.Selection([
        ('cash', 'Cash - نقدي'),
        ('credit', 'Credit - فاتورة آجلة'),
        ('bank', 'Bank - بانک'),
    ], required=True)

# class StockMove(models.Model):
#     _inherit = 'stock.move'
#
#     method = fields.Selection(
#         [('normal', 'Normal'), ('concrete', 'Concrete')],
#         string="Method",
#         required=True,
#         default='concrete'
#     )

class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    barcode = fields.Char(
        string='Barcode'
    )
    # opc = fields.Boolean(
    #     string='OPC'
    # )
    # src = fields.Boolean(
    #     string='SRC'
    # )
    # quantity_of_cement = fields.Float(
    #     'Quantity of Cement / m3'
    # )
    # clas = fields.Char(
    #     'Class'
    # )
    # total_loading = fields.Char(
    #     'Total Loading'
    # )
    # slump = fields.Char(
    #     'Slump'
    # )
    # temperature = fields.Char(
    #     'Temperature'
    # )
    # weight = fields.Char(
    #     'Weight'
    # )
    # pump = fields.Char(
    #     'Pump'
    # )
    # wc = fields.Char(
    #     'W/C'
    # )
    # method = fields.Char(
    #     'Method'
    # )