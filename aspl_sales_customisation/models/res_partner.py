# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class SaleType(models.Model):
    _inherit = 'res.partner'

    sales_type_id = fields.Many2one('sale.type', required=True, string='Sales Type')
