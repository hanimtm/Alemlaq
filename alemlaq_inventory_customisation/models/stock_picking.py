# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

class Picking(models.Model):
    _inherit = "stock.picking"

    state = fields.Selection(selection_add=[('clearance', 'Clearance'),
                                            ('under_transit', 'Under Transit'),
                                            ('waiting', 'Waiting Another Operation')],domain="[('picking_type_id.code', '=', 'incoming')]")

    is_clearance_order = fields.Boolean('Clearance Order?', copy=False, default=False)
    is_transit_order = fields.Boolean('Transit Order?', copy=False, default=False)

    def set_clearance_qty(self):
        # self.move_lines._set_quantities_to_reservation()
        if not self.product_imported and self.picking_type_id.code == 'incoming':
            raise ValidationError('Please upload the products first with Import Receipts')
        for picking_id in self:
            for move in picking_id.move_ids_without_package:
                move.clearance_qty = move.quantity_done
                move.clearance_user_id = picking_id.env.user.id or False
            picking_id.is_clearance_order = True
            picking_id.write({'state':'under_transit'})


    def set_transit_qty(self):
        for picking_id in self:
            for move in picking_id.move_ids_without_package:
                move.transit_qty = move.clearance_qty
                move.transit_user_id = picking_id.env.user.id or False
            picking_id.is_transit_order = True
            picking_id.write({'state': 'assigned'})