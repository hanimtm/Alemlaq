# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class AccountMoveLineInherit(models.Model):
    _inherit = "account.move.line"

    def create(self, vals_list):
        """ Super call for set account in Journal Items """
        res = super(AccountMoveLineInherit, self).create(vals_list)

        if res and res.move_id and res.move_id.invoice_origin:
            sale_order_id = self.env['sale.order'].search([('name', '=', res.move_id.invoice_origin)])
            if sale_order_id.sales_type_id and sale_order_id.sales_type_id.income_account:
                for line in res:
                    if line['debit'] > 0:
                        line['account_id'] = sale_order_id.sales_type_id.income_account.id
        return res



