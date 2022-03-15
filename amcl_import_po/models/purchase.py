# -*- coding: utf-8 -*-

from odoo import fields, models, api, _

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    #product_ids = fields.One2many('product.product', 'purchase_order', 'Products', required=True)

    import_wizard_id = fields.Char('Import Wizard ID')

    @api.depends('date_order', 'currency_id', 'company_id', 'company_id.currency_id')
    def _compute_currency_rate(self):
        for order in self:
            order.currency_rate = 0
            if order.currency_id.id != order.company_id.currency_id.id:
                order.currency_rate = self.env['res.currency']._get_conversion_rate(order.company_id.currency_id, order.currency_id, order.company_id, order.date_order)