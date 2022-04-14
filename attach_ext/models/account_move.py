from odoo import models, fields, _
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = 'account.move'

    transfer_no = fields.Char(string='Transfer Number')
    transfer_permit = fields.Binary(string='Transfer Permit')
    transfer_permit_filename = fields.Char(string='Transfer Permit')
    bank_name = fields.Char(string='Bank')

    # def action_post(self):
    #     res = super(AccountMove, self).action_post()
    #     if self.sale_order:
    #         if not self.transfer_permit:
    #             raise ValidationError(_('Transfer Permit is required, Please enter it before confirm invoice'))
    #     if not self.bank_name:
    #         raise ValidationError(_('Bank Name is required, Please enter it before confirm invoice'))
    #     if not self.payment_reference:
    #         raise ValidationError(_('Payment Reference is required, Please enter it before confirm invoice'))
    #     return res
