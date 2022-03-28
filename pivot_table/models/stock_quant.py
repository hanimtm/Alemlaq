from odoo import api, fields, models


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    product_name = fields.Char(related='product_id.name', store=True)
    product_default_code = fields.Char(related='product_id.default_code', store=True)
