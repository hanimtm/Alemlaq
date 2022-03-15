# -*- coding: utf-8 -*-

from odoo import api, models, fields, _


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    model_year = fields.Char('Model Year')
    grade = fields.Char('Grade (VC)')
    exterior_color_code = fields.Char('Exterior Color Code(VC)')
    exterior_color = fields.Char('Exterior Color (VC)')
    interior_color_code = fields.Char('Interior Color Code(VC)')
    interior_color = fields.Char('Interior Color (VC)')
    transmission_type = fields.Selection(
        [('automatic', 'AUTOMATIC'),
         ('cvt', 'CVT'),
         ('manual', 'MANUAL')],
        default='automatic', string="Transmission Type")

    brand = fields.Char('Brand')
    alj_suffix = fields.Char('ALJ Suffix (VC)')
    vehicle_model = fields.Char('Vehicle Model')
    complete_engine_number = fields.Char('Complete Engine Number')
    sales_document = fields.Char('Sales Document')
    item = fields.Char('Item')
    billing_document = fields.Char('Billing Document')
    bill_date = fields.Date('Bill Date')
    stock_location_id = fields.Many2one('stock.location', string="Location")