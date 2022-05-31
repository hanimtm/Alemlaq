# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import AccessError, UserError
import uuid


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    sequence_id = fields.Char('Sequence', default=lambda self: str(uuid.uuid4()))

    def _create_invoice(self, order, so_line, amount):
        if not self.env['account.move'].search([('sequence_id', '=', self.sequence_id)]):
            if (self.advance_payment_method == 'percentage' and self.amount <= 0.00) or (
                    self.advance_payment_method == 'fixed' and self.fixed_amount <= 0.00):
                raise UserError(_('The value of the down payment amount must be positive.'))

            amount, name = self._get_advance_details(order)

            invoice_vals = self._prepare_invoice_values(order, name, amount, so_line)
            invoice_vals['sequence_id'] = self.sequence_id
            if order.fiscal_position_id:
                invoice_vals['fiscal_position_id'] = order.fiscal_position_id.id

            invoice = self.env['account.move'].with_company(order.company_id) \
                .sudo().create(invoice_vals).with_user(self.env.uid)

            invoice.message_post_with_view('mail.message_origin_link',
                                           values={'self': invoice, 'origin': order},
                                           subtype_id=self.env.ref('mail.mt_note').id)
            return invoice
        else:
            return self.env['account.move'].search([('sequence_id', '=', self.sequence_id)])[0]
