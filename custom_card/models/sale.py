# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    custom_card_request_count = fields.Integer(
        string='Custom Cards', compute='_compute_custom_card_requests')

    sent_card_request = fields.Boolean(string='Sent Card Request?', default=False, copy=False)
    is_card_request_approved = fields.Boolean(string='Is Card Request Approved?', default=False, copy=False)

    def request_for_custom_card(self):
        custom_card_obj = self.env['custom.card.request']
        for order in self:
            if not order.sent_card_request:
                request_id = custom_card_obj.create({'partner_id':order.partner_id.id,
                                        'user_id':order.user_id.id,
                                        'sale_order_id':order.id,
                                        'state': 'draft'})

                for line in order.order_line:
                    request_id.write({'custom_card_request_ids': [(0,0, {'product_id':line.product_id.id,
                                                                                            'vin': line.product_id.default_code or "",
                                                                                            'custom_card_request_id':request_id.id})]})
                order.write({'sent_card_request':True})
        return True

    def _compute_custom_card_requests(self):
        for record in self:
            order_custom_card_request_ids = self.env['custom.card.request'].search([('sale_order_id','=',record.id)])
            record.custom_card_request_count = record and len(order_custom_card_request_ids.ids) or 0

    def action_view_custom_card_requests(self):
        self.ensure_one()
        form_view_ref = self.env.ref(
            'custom_card.custom_card_request_form_view', False)
        tree_view_ref = self.env.ref(
            'custom_card.custom_card_request_tree_view', False)
        result = self.env['ir.actions.act_window']._for_xml_id(
            'custom_card.action_request_custom_card')
        custom_card_request_order_ids = self.env['custom.card.request'].search([('sale_order_id','=',self.id)])
        result.update({
            'domain': [('id', 'in', custom_card_request_order_ids.ids)],
            'views': [(tree_view_ref.id, 'tree'), (form_view_ref.id, 'form')],
        })
        if len(custom_card_request_order_ids) == 1:
            result.update({
                'views': [
                    (form_view_ref.id, 'form'), (tree_view_ref.id, 'tree')],
                'res_id': custom_card_request_order_ids.ids[0],
            })
        return result

    def action_card_documents(self):
        custom_card_request_order_id = self.env['custom.card.request'].search([('sale_order_id', '=', self.id)],limit=1)
        return {
            'name': 'Card Document',
            'domain': [('id', 'in', custom_card_request_order_id.custom_card_request_ids.ids)],
            'type': 'ir.actions.act_window',
            'view_mode': 'tree',
            'res_model': 'custom.card.request.line',
            'view_id': self.env.ref('custom_card.custom_card_request_line_tree_view').id,
        }
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
