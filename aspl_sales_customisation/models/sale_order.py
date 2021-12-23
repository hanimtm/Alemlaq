# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class SaleType(models.Model):
    _inherit = 'sale.order'

    mobile_no = fields.Char(string='Mobile No', related='partner_id.mobile')
    e_mail = fields.Char(string='E-mail', related='partner_id.email')
    sales_type_id = fields.Many2one('sale.type', related='partner_id.sales_type_id', string='Sales Type')
