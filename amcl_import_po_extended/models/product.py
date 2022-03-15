# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class ProductTemplate(models.Model):
    _inherit = "product.template"

    exterior_color_code = fields.Char('Exterior Color Code (VC)')
    interior_color_code = fields.Char('Interior Color Code (VC)')
    key_number = fields.Char('Key Number')
    vessel_no = fields.Char('Vessel No.')
    card_no = fields.Char('Card No')
