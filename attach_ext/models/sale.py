# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)


class SaleType(models.Model):
    _inherit = 'sale.type'
    _description = 'add ext id'
    _sql_constraints = [
        ('uniq_name', 'unique(ext_id)', "This ext id already exists with this name . ext id name must be unique!"),
    ]

    ext_id = fields.Integer(string='Ext ID')


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    sale_type_ext_id = fields.Integer(related='sales_type_id.ext_id')
    customer_gender = fields.Selection(related='partner_id.customer_gender')

    id_card_iqama = fields.Binary(related='partner_id.id_card_iqama')
    id_card_iqama_filename = fields.Char(related='partner_id.id_card_iqama_filename')

    license_driving = fields.Binary(related='partner_id.license_driving')
    license_driving_filename = fields.Char(related='partner_id.license_driving_filename')
    #  اقرار عادي
    eqrar = fields.Binary(tracking=True, string='إقرار عادي')
    eqrar_filename = fields.Char(tracking=True)

    eqrar_woman = fields.Binary(tracking=True, string='إقرار تسجيل إمرأة')
    eqrar_woman_filename = fields.Char(tracking=True)

    # نموذج إستلام
    receipt_form = fields.Binary(tracking=True, string='نموذج إستلام')
    receipt_form_filename = fields.Char(tracking=True)
    # نموذج رقم 4 - تعهد الأفراد
    form_nb_four = fields.Binary(tracking=True, string='نموذج رقم 4 - تعهد الأفراد')
    form_nb_four_filename = fields.Char(tracking=True)

    # نموذج إقرار المستخدم
    user_acknowledgment = fields.Binary(tracking=True, string='نموذج إقرار المستخدم')
    user_acknowledgment_filename = fields.Char(tracking=True)

    # إقرار تسجيل مركبة بوكالة
    registration_agency = fields.Binary(tracking=True, string='إقرار تسجيل مركبة بوكالة')
    registration_agency_filename = fields.Char(tracking=True)

    # تفويض بتسجيل مركبة
    vehicle_registration = fields.Binary(tracking=True, string='تفويض بتسجيل مركبة')
    vehicle_registration_filename = fields.Char(tracking=True)

    cr = fields.Binary(related='partner_id.cr')
    cr_filename = fields.Char(related='partner_id.cr_filename')

    tax_certificate = fields.Binary(related='partner_id.tax_certificate')
    tax_certificate_filename = fields.Char(related='partner_id.tax_certificate_filename')

    national_address = fields.Binary(related='partner_id.national_address')
    national_address_filename = fields.Char(related='partner_id.national_address_filename')

    def notify_sticky(self):
        self.ensure_one()
        return {
            'type': 'ir.action.client',
            'tag': 'display_notification',
            'params': {
                'type': 'danger',
                'message': _('Field is required.'),
                'sticky': True
            }
        }

    @api.onchange('sales_type_id')
    def onchange_sales_type(self):
        if self.sales_type_id.ext_id != 1:
            self.customer_gender = 'woman'

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        if self.sale_type_ext_id == 1:
            condition = False
            message_id_card_iqama = ''
            message_license_driving = ''
            message_eqrar = ''
            message_eqrar_woman = ''
            if not self.id_card_iqama:
                condition = True
                message_id_card_iqama += _('\n-ID Card/Iqama')
            if not self.license_driving:
                condition = True
                message_license_driving += _('\n-License Driving')
            if not self.eqrar:
                condition = True
                message_eqrar += _('\n-Eqrar')
            if self.customer_gender == 'woman' and not self.eqrar_woman:
                condition = True
                message_eqrar_woman += _('\n-Eqrar Woman')
            if condition:
                full_message = _('That field is required\n')
                if message_id_card_iqama != '':
                    full_message += message_id_card_iqama
                if message_license_driving != '':
                    full_message += message_license_driving
                if message_eqrar != '':
                    full_message += message_eqrar
                if message_eqrar_woman != '':
                    full_message += message_eqrar_woman
                raise ValidationError(full_message)
        elif self.sale_type_ext_id in [2, 4]:
            message_cr = ''
            message_tax_certificate = ''
            message_national_address = ''
            condition = False
            if not self.cr:
                condition = True
                message_cr += _('\n-Commercial Registration')
            if not self.tax_certificate:
                condition = True
                message_tax_certificate += _('\n-Tax Certification')
            if not self.national_address:
                condition = True
                message_national_address += _('\n-National Address')
            if condition:
                full_message = _('That field is required\n')
                if message_cr != '':
                    full_message += message_cr
                if message_tax_certificate != '':
                    full_message += message_tax_certificate
                if message_national_address != '':
                    full_message += message_national_address
                raise ValidationError(full_message)
        return res


