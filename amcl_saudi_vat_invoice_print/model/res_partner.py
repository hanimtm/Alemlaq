# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    arabic = fields.Char(
        'Arabic Name'
    )
    district = fields.Char(
        'District'
    )
    cr_number = fields.Char(
        'CR Number'
    )
    customer_no = fields.Char(
        'Customer No.'
    )
    location = fields.Char(
        'Location.'
    )
    additional_no = fields.Char(
        'Additional No.'
    )
