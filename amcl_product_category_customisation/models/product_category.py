# -*- coding: utf-8 -*-

from odoo import fields, models , api, _


class Company(models.Model):
    _inherit = 'product.category'

    company_id = fields.Many2one('res.company', string='Company')
