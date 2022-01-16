# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class StockPicking(models.Model):
    _inherit = "stock.picking"

    product_imported = fields.Boolean('Product Imported')
    product_ids = fields.One2many('stock.receipt.line', 'picking_id', 'Product Details',compute='_compute_product_ids_lines',store=True)

    @api.depends('move_ids_without_package')
    def _compute_product_ids_lines(self):
        stock_receipt_line_obj = self.env['stock.receipt.line']
        stock_receipt_line_list = []
        for picking_id in self:
            if not picking_id.state == 'done':
                additional_product_vals = {}
                for line in picking_id.move_ids_without_package:
                    additional_product_vals = {'product_id': line.product_id.id,
                                               'description': line.product_id.description or "",
                                               'brand' : line.product_id.brand or "",
                                               'vin':line.product_id.default_code or " ",
                                                'exterior_color':line.product_id.exterior_color or "",
                                                'interior_color':line.product_id.interior_color or "",
                                                'complete_engine_number':line.product_id.complete_engine_number or " ",
                                                'model_code':line.product_id.model_code or "",
                                                'action':line.product_id.action or " ",
                                                'alj_suffix':line.product_id.alj_suffix or "",
                                                'model_year':line.product_id.model_year or "",
                                                'grade':line.product_id.grade or " ",
                                                'transmission_type':line.product_id.transmission_type or "",
                                                'sales_document':line.product_id.sales_document or "",
                                                'request_delivery_date':line.product_id.request_delivery_date or False,
                                                'billing_document':line.product_id.billing_document or "",
                                                'bill_date':line.product_id.bill_date or False,
                                                'vehicle_wholesale_price':line.product_id.vehicle_wholesale_price or 0.0,
                                                'broker_declaration_date': line.product_id.broker_declaration_date or False,
                                                'declaration_date':line.product_id.declaration_date or False,
                                                'netval':line.product_id.netval or "",
                                                'vat_amount':line.product_id.vat_amount or ""}
                    stock_receipt_line=stock_receipt_line_obj.create(additional_product_vals)
                    stock_receipt_line_list.append(stock_receipt_line.id)
                if stock_receipt_line_list:
                    if not picking_id.product_ids:
                        picking_id.sudo().write({'product_ids': [(6, 0, stock_receipt_line_list)] or []})
        return True


    def button_validate(self):
        if not self.product_imported and self.picking_type_id.code == 'incoming':
            raise ValidationError('Please upload the products and then try to validate')
        validate = super(StockPicking, self).button_validate()
        if self.product_imported and self.picking_type_id.code == 'incoming':
            for line in self.product_ids:
                line.product_id.write({
                    'brand': line.brand,
                    'description': line.description,
                    'exterior_color': line.exterior_color,
                    'interior_color': line.interior_color,
                    'complete_engine_number': line.complete_engine_number,
                    'model_code': line.model_code,
                    'action': line.action,
                    'alj_suffix': line.alj_suffix,
                    'model_year': line.model_year,
                    'grade': line.grade,
                    'transmission_type': line.transmission_type,
                    'sales_document': line.sales_document,
                    'request_delivery_date': line.request_delivery_date,
                    'billing_document': line.billing_document,
                    'bill_date': line.bill_date,
                    'vehicle_wholesale_price': line.vehicle_wholesale_price,
                    'broker_declaration_date': line.broker_declaration_date,
                    'declaration_date': line.declaration_date,
                    'netval': line.netval,
                    'vat_amount': line.vat_amount,
                })
        return validate


class StockReceiptLine(models.Model):
    _name = 'stock.receipt.line'
    _description = 'Stock Picking Line'

    picking_id = fields.Many2one('stock.picking', 'Picking')
    brand = fields.Char('Brand')
    product_id = fields.Many2one('product.product', 'Product')
    description = fields.Char('Description')
    vin = fields.Char('VIN')
    exterior_color = fields.Char('Exterior Color (VC)')
    interior_color = fields.Char('Interior Color (VC)')
    complete_engine_number = fields.Char('Complete Engine Number')
    model_code = fields.Char('Model Code')
    action = fields.Char('Action')
    alj_suffix = fields.Char('ALJ Suffix (VC)')
    model_year = fields.Char('Model Year')
    grade = fields.Char('Grade (VC)')
    transmission_type = fields.Selection(
        [('automatic', 'AUTOMATIC'),
         ('cvt', 'CVT'),
         ('manual', 'MANUAL')],
        default='automatic', string="Transmission Type")
    sales_document = fields.Char('Sales Document')
    request_delivery_date = fields.Date('Request Delivery Date')
    billing_document = fields.Char('Billing Document')
    bill_date = fields.Date('Bill Date')
    vehicle_wholesale_price = fields.Float('Vehicle Wholesale Price')
    broker_declaration_date = fields.Date('Broker Declaration Date')
    declaration_date = fields.Date('Declaration Date')
    netval = fields.Float('Net Val')
    vat_amount = fields.Float('VAT Amount')






