# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def button_confirm(self):
        res = super(PurchaseOrder, self).button_confirm()
        for picking_id in self.picking_ids:
            picking_id.write({'state': "clearance"})
        return res
