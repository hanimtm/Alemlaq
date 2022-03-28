from odoo import fields, models


class StockLocation(models.Model):
    _inherit = 'stock.location'
    _order = 'location_sequence'

    location_sequence = fields.Integer(string='Sequence')

