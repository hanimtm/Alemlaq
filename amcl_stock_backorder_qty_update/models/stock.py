# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class StockBackorderConfirmation(models.TransientModel):
    _inherit = 'stock.backorder.confirmation'

    def process_cancel_backorder(self):
        pickings_to_validate = self.env.context.get('button_validate_picking_ids')

        for picks in pickings_to_validate:
            pick = self.env['stock.picking'].browse(picks)
            print('pickings_to_validate :: ', pick)
            for move in pick.move_ids_without_package:
                if move.product_uom_qty == 0:
                    self.env.cr.execute('delete from purchase_order_line where id=%s', (move.purchase_line_id.id,))
                    move.sudo().unlink()
                elif move.product_uom_qty != move.quantity_done:
                    move.purchase_line_id.write({'product_qty': move.quantity_done})
                    move.purchase_line_id._compute_amount()
        if pickings_to_validate:
            return self.env['stock.picking'] \
                .browse(pickings_to_validate) \
                .with_context(skip_backorder=True, picking_ids_not_to_backorder=self.pick_ids.ids) \
                .button_validate()
        return True
