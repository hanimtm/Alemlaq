# -*- coding: utf-8 -*-

from odoo import fields, models , api, _


class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'

    # allowed_user_ids = fields.Many2many('res.users', string='Allowed Users')
    allowed_users = fields.Many2many('res.users', string='Allowed Users')

