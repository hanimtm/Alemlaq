from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = 'stock.move'

    brand = fields.Char('Brand')
    description = fields.Char('Description')
    vin = fields.Char('VIN')
    exterior_color = fields.Char('Exterior Color (VC)')
    exterior_color_code = fields.Char('Exterior Color Code (VC)')
    interior_color = fields.Char('Interior Color (VC)')
    interior_color_code = fields.Char('Interior Color Code (VC)')
    complete_engine_number = fields.Char('Complete Engine Number')
    model_code = fields.Char('Model Code')

    alj_suffix = fields.Char('ALJ Suffix (VC)')
    model_year = fields.Char('Model Year')
    grade = fields.Char('Grade (VC)')
    transmission_type = fields.Selection(
        [('automatic', 'AUTOMATIC'),
         ('cvt', 'CVT'),
         ('manual', 'MANUAL')],
        default='automatic', string="Transmission Type")
    sales_document = fields.Char('Sales Document')
    billing_document = fields.Char('Billing Document')
    bill_date = fields.Date('Bill Date')
    key_number = fields.Char('Key Number')
    vessel_no = fields.Char('Vessel No.')
    card_no = fields.Char('Card No')

    # action = fields.Char('Action')
    # request_delivery_date = fields.Date('Request Delivery Date')
    # vehicle_wholesale_price = fields.Float('Vehicle Wholesale Price')
    # broker_declaration_date = fields.Date('Broker Declaration Date')
    # declaration_date = fields.Date('Declaration Date')
    # netval = fields.Float('Net Val')
    # vat_amount = fields.Float('VAT Amount')

    @api.model
    def create(self, vals):
        res = super(StockMove, self).create(vals)
        purchase_line = vals.get('purchase_line_id')
        sale_line = vals.get('sale_line_id')
        order_line_id = False
        if purchase_line:
            order_line_id = self.env['purchase.order.line'].browse(purchase_line)
        if sale_line:
            order_line_id = self.env['sale.order.line'].browse(sale_line)

        if order_line_id:
            res.write({'brand': order_line_id.product_id.brand or "",
                   'description': order_line_id.product_id.description or "",
                   'vin': order_line_id.product_id.default_code or "",
                   'exterior_color': order_line_id.product_id.exterior_color or "",
                   'exterior_color_code': order_line_id.product_id.exterior_color_code or "",
                   'interior_color': order_line_id.product_id.interior_color or "",
                   'interior_color_code': order_line_id.product_id.interior_color_code or "",
                   'complete_engine_number': order_line_id.product_id.complete_engine_number or "",
                   'model_code': order_line_id.product_id.model_code or "",
                   #'action': order_line_id.product_id.action or "",
                   'alj_suffix': order_line_id.product_id.alj_suffix or "",
                   'model_year': order_line_id.product_id.model_year or "",
                   'grade': order_line_id.product_id.grade or "",
                   'transmission_type': order_line_id.product_id.transmission_type or "",
                   'sales_document': order_line_id.product_id.sales_document or "",
                   #'request_delivery_date': order_line_id.product_id.request_delivery_date or False,
                   'billing_document': order_line_id.product_id.billing_document or "",
                   #'vehicle_wholesale_price': order_line_id.product_id.vehicle_wholesale_price or "",
                   #'broker_declaration_date': order_line_id.product_id.broker_declaration_date or False,
                   #'declaration_date': order_line_id.product_id.declaration_date or False,
                   #'netval': order_line_id.product_id.netval or "",
                   #'vat_amount': order_line_id.product_id.vat_amount or "",
                   })
        return res



