# -*- coding: utf-8 -*-

# Part of Probuse Consulting Service Pvt Ltd. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
import logging

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    license_plate_ids = fields.One2many('license.plate', 'sale_order_id', string='License Plate')

    def btn_open_wizard_create_new_license_plate(self):
        self.ensure_one()
        res = {
            'type': 'ir.actions.act_window',
            'name': _('Create New License Plate'),
            'res_model': 'license.plate.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            # 'view_id': view_id,
            'view_id': self.env.ref("offer_price.license_plate_wizard_view_form").id,
            'target': 'new',
            'context': {
                'default_sale_order_id': self.id
            }
        }
        return res


# class SaleOrderLine(models.Model):
#     _inherit = 'sale.order.line'
#
#     price_after_tax = fields.Float(compute='_compute_price_after_taxes', store=True)
#
#     @api.depends('tax_id')
#     def _compute_price_after_taxes(self):
#         for line in self:
#             line.price_after_tax = 0
#             for tax in line.tax_id:
#                 # raise ValidationError(str(tax.amount))
#                 line.price_after_tax += tax.amount
