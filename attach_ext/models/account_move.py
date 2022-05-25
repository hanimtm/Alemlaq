from odoo import models, fields, _, api
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'

    transfer_no = fields.Char(string='Transfer Number')
    transfer_permit = fields.Binary(string='Transfer Permit')
    transfer_permit_filename = fields.Char(string='Transfer Permit')
    bank_name = fields.Many2one(comodel_name='account.journal', string='Bank',
                                domain="[('type', '=', 'bank')]")

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
