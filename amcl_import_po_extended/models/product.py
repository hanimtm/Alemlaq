# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class ProductTemplate(models.Model):
    _inherit = "product.template"

    exterior_color_code = fields.Char('Exterior Color Code (VC)')
    interior_color_code = fields.Char('Interior Color Code (VC)')
