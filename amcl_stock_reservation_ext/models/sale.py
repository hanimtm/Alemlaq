# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
import logging
_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_create_stock_reservation_direct(self):
        custome_reservtion_obj = self.env['stock.move.reservation']
        location_obj = self.env['stock.location']
        picking_type_obj = self.env['stock.picking.type']
        move_id_generated = False
        mail_context = []

        for line in self.order_line:
            print(line.product_id.is_reservation)
            if line.product_uom_qty > 0 and line.product_id.detailed_type != 'service' and not line.product_id.is_reservation:

                order_line_reserve_qty = line.product_uom_qty
                order_line_reserve_qty += line.product_uom_qty

                if line.product_uom_qty >= 1:
                    picking_type_id = picking_type_obj.search([
                        ('warehouse_id', '=', self.warehouse_id.id),
                        ('code', '=', 'outgoing')],
                        limit=1
                    )
                    location_id = picking_type_id.default_location_src_id
                    # location_dest_id = self.env.ref("odoo_stock_reservation.stock_dest_location_reservation")
                    location_dest_id = self.env['stock.location'].search([
                        ('is_stock_location_reservation', '=', True),
                        ('company_id', '=', self.company_id.id)], limit=1)

                    reserv_move_id = custome_reservtion_obj.create({
                        'name': line.name,
                        'custome_so_line_id': line.id,
                        'product_id': line.product_id.id,
                        'product_uom_qty': line.product_uom_qty,
                        'product_uom': line.product_uom.id,
                        'location_id': location_id.id,
                        'location_dest_id': location_dest_id.id,
                        'custome_sale_order_id': self.id,
                        'reserv_request_date': fields.Datetime.now(),
                        'reserv_resquest_user_id': self.env.uid,
                    })

                    if reserv_move_id:
                        # line.stock_reserved_qty += line.pro
                        self.is_stock_reserv_created = True
                        mail_context.append({
                            'name': reserv_move_id.reserv_code,
                            'product_id': reserv_move_id.product_id,
                            'reserved_qty': reserv_move_id.product_uom_qty,
                        })
                        reserv_move_id.move_id._action_confirm()
                        move_id_generated = True
                    line.product_id.write({'is_reservation': True, 'reserver_id': self.env.user.id})
                else:
                    raise ValidationError("All the quantities are reserved")


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
