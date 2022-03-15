# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import AccessError, UserError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('price_unit')
    def onchange_unit_price_change(self):
        margin = self.env['global.margin'].search([])[0]
        print(margin.global_margin)
        if margin.global_margin > 0 and self.env.user.has_group(
                'sales_team.group_sale_salesman') and (
                not self.env.user.has_group('sales_team.group_sale_manager') or not self.env.user.has_group(
            'base.group_erp_manager')):
            after_margin = self.product_id.standard_price + (self.product_id.standard_price * margin.global_margin) / 100
            print(after_margin)
            if (self.price_unit != 0 and self.price_unit <= after_margin) or (self.price_unit != 0 and self.price_unit <= self.product_id.standard_price):
                raise UserError(
                    _('You can not enter a Unit Price, which is less or equal to marginal amount or less than the cost.'))
