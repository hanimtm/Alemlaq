from odoo import fields, models, api, _
from odoo.exceptions import AccessError, UserError
import uuid


class AccountMove(models.Model):
    _inherit = "account.move"

    sequence_id = fields.Char('Sequence ID')


class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    sequence_id = fields.Char('Sequence', default=lambda self: str(uuid.uuid4()))

    def _create_payment_vals_from_wizard(self):
        payment_vals = super()._create_payment_vals_from_wizard()
        payment_vals['sequence_id'] = self.sequence_id
        return payment_vals

    def action_create_payments(self):
        if not self.env['account.payment'].search([('sequence_id', '=', self.sequence_id)]):
            payments = self._create_payments()
        else:
            payments = self.env['account.payment'].search([('sequence_id', '=', self.sequence_id)])

        if self._context.get('dont_redirect_to_payments'):
            return True

        action = {
            'name': _('Payments'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.payment',
            'context': {'create': False},
        }
        if len(payments) == 1:
            action.update({
                'view_mode': 'form',
                'res_id': payments.id,
            })
        else:
            action.update({
                'view_mode': 'tree,form',
                'domain': [('id', 'in', payments.ids)],
            })
        return action

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    sequence_id = fields.Char('Sequence ID')
