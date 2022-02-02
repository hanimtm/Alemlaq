# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    #product_ids = fields.One2many('product.product', 'purchase_order', 'Products', required=True)

    import_wizard_id = fields.Char('Import Wizard ID')