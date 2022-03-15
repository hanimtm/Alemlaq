from odoo import fields, models, api


class LicensePlate(models.Model):
    _name = 'license.plate'

    product_id = fields.Many2one('product.product', string='License Plate')
    qty = fields.Integer(default=1)
    order_line_id = fields.Many2one('sale.order.line', string='Order Line')
    price = fields.Float('Unit Price')
    sale_order_id = fields.Many2one('sale.order', string='Sale Order', ondelete='cascade')
