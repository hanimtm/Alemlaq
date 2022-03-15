# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class StockMove(models.Model):
    _inherit = "stock.move"

    clearance_qty = fields.Float('Clearance Quantity',digits='Product Unit of Measure', states={'done': [('readonly', True)]})
    transit_qty = fields.Float('Transit Quantity', digits='Product Unit of Measure',
                                 states={'done': [('readonly', True)]})

    clearance_user_id = fields.Many2one('res.users',string='Clearance User Name',default=lambda self: self.env.user)
    transit_user_id = fields.Many2one('res.users', string='Transit User Name',default=lambda self: self.env.user)
    final_user_id = fields.Many2one('res.users', string='Final User Name', default=lambda self: self.env.user)

    # def set_clearance_qty(self):
    #     print("Hello")
    #     return
    #
    # def set_transit_qty(self):
    #     print("Hello")
    #     return
