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

    # @api.model
    # def create(self, vals):
    #     company_id = vals.get('company_id', self.default_get(['company_id'])['company_id'])
    #     # Ensures default picking type and currency are taken from the right company.
    #     self_comp = self.with_company(company_id)
    #     print('import_wizard_id 1:: ',  vals.get('import_wizard_id'))
    #     print('import_wizard_id 2:: ', self.import_wizard_id)
    #     created_po = self.env['purchase.order'].sudo().search(
    #         [('import_wizard_id', '=', vals.get('import_wizard_id'))])
    #     res = super(PurchaseOrder, self_comp).create(vals)
    #     return res
