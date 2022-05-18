from odoo import fields, api, models
import logging

_logger = logging.getLogger(__name__)

class LicensePlateWizard(models.TransientModel):
    _name = 'license.plate.wizard'

    product_id = fields.Many2one('product.product', string='License Plate')
    order_line_id = fields.Many2one('sale.order.line', string='Order Line',
                                    domain="[('order_id', '=', 'sale_order_id')]")
    qty = fields.Integer(default=1, readonly=1)
    sale_order_id = fields.Many2one('sale.order', string='Sale Order')

    def create_new_license_plate(self):
        licenses_plate = self.env['license.plate'].search(
            [('product_id', '=', self.product_id.id),
             ('sale_order_id', '=', self.sale_order_id.id),
             ('order_line_id', '=', self.order_line_id.id)])
        _logger.critical('License Plate****')
        _logger.critical(licenses_plate)
        i=0
        if not licenses_plate:
            _logger.critical(str(i+1))
            license_plate = self.env['license.plate'].create({
                'product_id': self.product_id.id,
                'qty': self.qty,
                'order_line_id': self.order_line_id.id,
                'price': self.product_id.list_price * self.qty,
                'sale_order_id': self.sale_order_id.id,
            })
            return license_plate
