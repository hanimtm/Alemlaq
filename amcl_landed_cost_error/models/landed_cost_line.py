# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.onchange('is_landed_costs_line', 'product_id')
    def _onchange_is_landed_costs_line_new(self):
        if self.product_id:
            accounts = self.product_id.product_tmpl_id._get_product_accounts()
            if self.product_type != 'service':
                self.account_id = accounts['expense']
                self.is_landed_costs_line = False
            elif self.is_landed_costs_line and self.move_id.company_id.anglo_saxon_accounting:
                if accounts['stock_input']:
                    self.account_id = accounts['stock_input']
                else:
                    self.account_id = self.product_id.property_account_income_id.id
            else:
                if accounts['expense']:
                    self.account_id = accounts['expense']
                else:
                    self.account_id = self.product_id.property_account_expense_id.id
