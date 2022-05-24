# -*- coding: utf-8 -*-

# Part of Probuse Consulting Service Pvt Ltd. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
import logging
_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_stock_reservation_order = fields.Boolean(
        string="Apply Stock Reservation?",
        copy=False,
    )
    stock_move_ids = fields.One2many(
        'stock.move.reservation',
        'custome_sale_order_id',
        string="Stock Reservations",
        copy=False,
    )

    is_stock_reserv_created = fields.Boolean(
        string="Is Stock Created",
        copy=False,
    )

    def action_confirm(self):
        for order in self:
            order_line = order.order_line
            stock_move_reservation_ids = self.env['stock.move.reservation'].search([
                ('custome_so_line_id', 'in', order_line.ids),
                ('state', '!=', 'cancel')
            ])
            if stock_move_reservation_ids:
                # raise ValidationError("Please Cancel Reserved Stock")
                self.action_cancel_stock_reservation()
        return super(SaleOrder, self).action_confirm()

    def action_create_stock_reservation(self):
        self.ensure_one()
        return {
            'name': _('Stock Reservation'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'stock.reservation',
            'view_id': self.env.ref('odoo_stock_reservation.wiz_stock_reservation_view').id,
            'type': 'ir.actions.act_window',
            'context': {
                'default_sale_order_id': self.id,
                'current_sale_order_id': self.id,
            },
            'target': 'new'
        }

    def action_cancel_stock_reservation(self):
        self.ensure_one()
        order_line_ids = self.order_line
        stock_move_reservation_ids = self.env['stock.move.reservation'].search([
            ('custome_so_line_id', 'in', order_line_ids.ids),
            ('state', '!=', 'cancel')
        ])
        stock_move_ids = self.env['stock.move']
        for move_res in stock_move_reservation_ids:
            stock_move_ids += move_res.move_id
        if stock_move_ids:
            result = stock_move_ids._action_cancel()
            if result:
                order_line_ids.write({
                    'stock_reserved_qty': 0.0,

                })
                # ****************************************
                # 'product_id.is_reservation': False
                order_line_ids.product_id.write({'is_reservation': False, 'reserver_id': False})
                # ****************************************
                self.is_stock_reserv_created = False
            return {
                'type': 'ir.actions.client',
                'tag': 'reload',
            }
        else:
            if not self._context.get('is_unlink_reserved_stock'):
                return {
                    'type': 'ir.actions.client',
                    'tag': 'reload',
                }
                # raise ValidationError("No any stock reservation records found.")

    def action_cancel(self):
        self.ensure_one()
        order_line_ids = self.order_line
        stock_move_reservation_ids = self.env['stock.move.reservation'].search([
            ('custome_so_line_id', 'in', order_line_ids.ids),
        ])
        if stock_move_reservation_ids:
            ctx = self._context.copy()
            ctx.update({'is_unlink_reserved_stock': True})
            self.with_context(ctx).action_cancel_stock_reservation()
            #            self.action_cancel_stock_reservation()
            stock_move_reservation_ids.unlink()
        return super(SaleOrder, self).action_cancel()

    def action_view_reserved_stock(self):
        self.ensure_one()
        action = self.env.ref("odoo_stock_reservation.action_stock_move_reserv_product").sudo().read()[0]
        action['domain'] = [('id', 'in', self.stock_move_ids.ids)]
        return action

    def schedule_action_cancel_reservation(self):
        # ICPSudo = self.env['ir.config_parameter'].sudo()
        # nb_days = ICPSudo.get_param('odoo_stock_reservation.nb_days')
        nb_days = 0
        if self.env['number.days.reservation'].search([])[0]:
            nb_days = self.env['number.days.reservation'].search([])[0].nb_days
        date_obj = fields.Date.today() - relativedelta(days=int(nb_days))
        sales = self.env['sale.order'].search([('validity_date', '=', date_obj)])
        for sale in sales:
            sale.action_cancel_stock_reservation()

    def _create_invoices(self, grouped=False, final=False, date=None):
        for line in self.order_line:
            if line.is_reservation:
                raise ValidationError("Can't create invoice because in this sale there is line reserved")
        return super(SaleOrder, self)._create_invoices()

    # @api.model
    # def create(self, vals):
    #     res = super(SaleOrder, self).create(vals)
    #
    #     custome_reservtion_obj = self.env['stock.move.reservation']
    #     location_obj = self.env['stock.location']
    #     picking_type_obj = self.env['stock.picking.type']
    #     move_id_generated = False
    #     mail_context = []
    #
    #     for line in vals['order_line']:
    #         _logger.critical('*********************')
    #         _logger.critical(line.product_id.name)
    #         # if line.stock_reservation_qty > 0.0 and line.product_qty >= line.stock_reservation_qty:
    #         # order_line_reserve_qty = line.order_line_id.stock_reserved_qty
    #         # order_line_reserve_qty += line.stock_reservation_qty
    #
    #         # if line.order_line_id.product_uom_qty >= order_line_reserve_qty:
    #         picking_type_id = picking_type_obj.search([
    #             ('warehouse_id', '=', vals['warehouse_id']),
    #             ('code', '=', 'outgoing')],
    #             limit=1
    #         )
    #         location_id = picking_type_id.default_location_src_id
    #         # location_dest_id = self.env.ref("odoo_stock_reservation.stock_dest_location_reservation")
    #         location_dest_id = self.env['stock.location'].search([
    #             ('is_stock_location_reservation', '=', True),
    #             ('company_id', '=', vals['company_id'])], limit=1)
    #
    #         reserv_move_id = custome_reservtion_obj.create({
    #             'name': vals['name'],
    #             'custome_so_line_id': res.id,
    #             'product_id': line.product_id.id,
    #             'product_uom_qty': line.stock_reservation_qty,
    #             'product_uom': line.uom_id.id,
    #             'location_id': location_id.id,
    #             'location_dest_id': location_dest_id.id,
    #             'custome_sale_order_id': self.sale_order_id.id,
    #             'reserv_request_date': fields.Datetime.now(),
    #             'reserv_resquest_user_id': self.env.uid,
    #             'reserved_qty': 1
    #         })
    #
    #         # if reserv_move_id:
    #         #     line.stock_reserved_qty += line.stock_reservation_qty
    #         #     self.sale_order_id.is_stock_reserv_created = True
    #         #     mail_context.append({
    #         #         'name': reserv_move_id.reserv_code,
    #         #         'product_id': reserv_move_id.product_id,
    #         #         'reserved_qty': reserv_move_id.product_uom_qty,
    #         #     })
    #         reserv_move_id.move_id._action_confirm()
    #         # move_id_generated = True
    #         line.product_id.write({'is_reservation': True, 'reserver_id': self.env.user.id})
    #         # else:
    #         #     raise ValidationError("All the quantities are reserved")
    #         # else:
    #         #     raise ValidationError("Quantity is less then 0.0 or reserved quantity more then Order Quantity")
    #
    #     # if self.user_ids and move_id_generated:
    #     #     partner_lst = [(4, user.partner_id.id) for user in self.user_ids]
    #     #     email_template_id = self.env.ref("odoo_stock_reservation.email_template_stock_reservation1")
    #     #     ctx = self._context.copy()
    #     #     ctx.update({'stock_reservation_ctx': mail_context})
    #     #     if email_template_id:
    #     #         email_template_id.with_context(ctx).send_mail(
    #     #             self.sale_order_id.id, email_values={'recipient_ids': partner_lst})
    #
    #     return res

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    stock_reserved_qty = fields.Float(
        string="Stock Reserved Quantity"
    )

    is_reservation = fields.Boolean(related="product_id.is_reservation")
    reserver_id = fields.Many2one(related="product_id.reserver_id",string="Reserved By")



    def write(self, vals):
        if 'product_id' in vals:
            for rec in self:
                stock_move_reservation_ids = self.env['stock.move.reservation'].search([
                    ('custome_so_line_id', '=', rec.id),
                    ('state', '!=', 'cancel')
                ])
                stock_move_ids = self.env['stock.move']
                for move_res in stock_move_reservation_ids:
                    stock_move_ids += move_res.move_id
                if stock_move_ids:
                    result = stock_move_ids._action_cancel()
                    if result:
                        vals.update(stock_reserved_qty=0.0)
        #                        vals.update(is_stock_reserv_created=True)
        return super(SaleOrderLine, self).write(vals)


    def unlink(self):
        for rec in self:
            stock = self.env['stock.move.reservation'].search([('custome_so_line_id', '=', rec.id)])
            stock_res_move_ids = stock.mapped('move_id')
            stock_res_move_ids._action_cancel()
            stock.unlink()
        return super(SaleOrderLine, self).unlink()

    @api.onchange('product_id')
    def _onchange_product_id(self):
        for line in self:
            if line.product_id.is_reservation:
                product = line.product_id.name
                reserver = line.product_id.reserver_id.name
                line.unlink()
                raise ValidationError(
                    _('The product %s is already reserved by %s, Please contact him to cancel the reservation to proceed.') % (
                        product, reserver))

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
