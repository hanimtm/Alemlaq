from odoo import fields, api, models


class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'

    user_ids = fields.Many2many(
        comodel_name='res.users', rel='rel_user_picking_type',
        column1='picking_type_id', column2='user_id', string='Users')


class StockLocation(models.Model):
    _inherit = 'stock.location'

    user_ids = fields.Many2many(
        comodel_name='res.users', rel='rel_user_stock_location',
        column1='location_id', column2='user_id', string='Users')
