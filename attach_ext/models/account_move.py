from odoo import models, fields, _, api
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    transfer_no = fields.Char(string='Transfer Number')
    transfer_permit = fields.Binary(string='Transfer Permit')
    transfer_permit_filename = fields.Char(string='Transfer Permit')


class PaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    transfer_no = fields.Char(string='Transfer Number')
    transfer_permit = fields.Binary(string='Transfer Permit')
    transfer_permit_filename = fields.Char(string='Transfer Permit')
    # bank_name = fields.Many2one(comodel_name='account.journal', string='Bank',
    #                             domain="[('type', '=', 'bank')]")

    # def _create_payment_vals_from_batch(self, batch_result):
    #     batch_values = self._get_wizard_values_from_batch(batch_result)
    #     return {
    #         'date': self.payment_date,
    #         'amount': batch_values['source_amount_currency'],
    #         'payment_type': batch_values['payment_type'],
    #         'partner_type': batch_values['partner_type'],
    #         'ref': self._get_batch_communication(batch_result),
    #         'journal_id': self.journal_id.id,
    #         'currency_id': batch_values['source_currency_id'],
    #         'partner_id': batch_values['partner_id'],
    #         'partner_bank_id': batch_result['payment_values']['partner_bank_id'],
    #         'payment_method_line_id': self.payment_method_line_id.id,
    #         'destination_account_id': batch_result['lines'][0].account_id.id
    #     }

    def _create_payment_vals_from_batch(self, batch_result):
        _logger.critical('3333333333333333333333333333333')
        res = super(PaymentRegister, self)._create_payment_vals_from_batch(batch_result)
        # if self.env.context.get('active_model') == 'account.move' and self.env.context.get('active_ids'):
        #     move_ids = self.env['account.move'].search([('id', 'in', self.env.context.get('active_ids'))])
        #     check_branch_diff = set([x.branch_id.id for x in move_ids])
        #     if len(check_branch_diff) > 1:
        #         raise UserError(_("Cannot create payment for different branches."))
        #     elif len(check_branch_diff) == 1:
        _logger.critical('**********************************')
        _logger.critical(batch_result)
        res['transfer_no'] = self.transfer_no
        res['transfer_permit'] = self.transfer_permit
        res['transfer_permit_filename'] = self.transfer_permit_filename
        return res

    def _create_payment_vals_from_wizard(self):
        res = super(PaymentRegister, self)._create_payment_vals_from_wizard()
        res['transfer_no'] = self.transfer_no
        res['transfer_permit'] = self.transfer_permit
        res['transfer_permit_filename'] = self.transfer_permit_filename
        return res

class AccountMove(models.Model):
    _inherit = 'account.move'

    # transfer_no = fields.Char(string='Transfer Number')
    # transfer_permit = fields.Binary(string='Transfer Permit')
    # transfer_permit_filename = fields.Char(string='Transfer Permit')
    # bank_name = fields.Many2one(comodel_name='account.journal', string='Bank',
    #                             domain="[('type', '=', 'bank')]")

    id_card_iqama = fields.Binary(compute='get_data_from_quotation')
    id_card_iqama_filename = fields.Char(compute='get_data_from_quotation')
    license_driving = fields.Binary(compute='get_data_from_quotation')
    license_driving_filename = fields.Char(compute='get_data_from_quotation')
    eqrar = fields.Binary(compute='get_data_from_quotation')
    eqrar_filename = fields.Char(compute='get_data_from_quotation')
    eqrar_woman = fields.Binary(compute='get_data_from_quotation')
    eqrar_woman_filename = fields.Char(compute='get_data_from_quotation')

    cr = fields.Binary(compute='get_data_from_quotation')
    cr_filename = fields.Char(compute='get_data_from_quotation')
    tax_certificate = fields.Binary(compute='get_data_from_quotation')
    tax_certificate_filename = fields.Char(compute='get_data_from_quotation')
    national_address = fields.Binary(compute='get_data_from_quotation')
    national_address_filename = fields.Char(compute='get_data_from_quotation')

    @api.depends('invoice_origin')
    def get_data_from_quotation(self):
        for rec in self:
            quotation = self.env['sale.order'].search([('name', '=', rec.invoice_origin)])
            driving = self.env['license.plate'].search([('sale_order_id.name', '=', rec.invoice_origin)])
            # if driving:
            #     # _logger.critical('*************************')
            #     # _logger.critical(driving.product_id.product_tmpl_id.name)
            #     # _logger.critical(rec.id)
            #     self.env['account.move.line'].sudo().create({
            #         # 4101001001
            #         'move_id': 1,
            #         'account_id': 1,
            #         'name': driving.product_id.product_tmpl_id.name,
            #         'debit': 0,
            #         'credit': driving.price
            #     })
            rec.id_card_iqama = quotation.id_card_iqama
            rec.id_card_iqama_filename = quotation.id_card_iqama_filename
            rec.license_driving = quotation.license_driving
            rec.license_driving_filename = quotation.license_driving_filename
            rec.eqrar = quotation.eqrar
            rec.eqrar_filename = quotation.eqrar_filename
            rec.eqrar_woman = quotation.eqrar_woman
            rec.eqrar_woman_filename = quotation.eqrar_woman_filename
            rec.cr = quotation.cr
            rec.cr_filename = quotation.cr_filename
            rec.tax_certificate = quotation.tax_certificate
            rec.tax_certificate_filename = quotation.tax_certificate_filename
            rec.national_address = quotation.national_address
            rec.national_address_filename = quotation.national_address_filename

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
