# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)


class AbstractBankReport(models.AbstractModel):
    _name = 'report.attach_ext.report_sale_order_rajhi_bank_view'

    @api.model
    def _get_report_values(self, docids, data=None):
        doc_id = data['id']
        model = data['model']
        doc = self.env[data['model']].browse(doc_id)
        docargs = {
            'doc_ids': [doc_id],
            'doc_model': model,
            'data': data,
            'docs': [doc],
        }
        return docargs


class SaleType(models.Model):
    _inherit = 'sale.type'
    _description = 'add ext id'
    _sql_constraints = [
        ('uniq_name', 'unique(ext_id)', "This ext id already exists with this name . ext id name must be unique!"),
    ]

    ext_id = fields.Integer(string='Ext ID')
    auto_reservation = fields.Boolean(default=False)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    partner_tax = fields.Char(related='partner_id.vat', store=1)

    sale_type_ext_id = fields.Integer(related='sales_type_id.ext_id', store=1)
    auto_reservation = fields.Boolean(related='sales_type_id.auto_reservation', store=1)
    customer_gender = fields.Selection(related='partner_id.gender')

    car_user_id = fields.Many2one(comodel_name='res.partner', string='Car User')

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

    # @api.onchange('partner_id')
    # def onchange_partner(self):
    #     if self.partner_id:
    #         # self.customer_gender = self.partner_id.gender
    #         if self.partner_id.company_type == 'person':
    #             self.id_card_iqama = self.partner_id.id_card_iqama
    #             self.id_card_iqama_filename = self.partner_id.id_card_iqama_filename
    #             self.license_driving = self.partner_id.license_driving
    #             self.license_driving_filename = self.partner_id.license_driving_filename
    #         else:
    #             self.cr = self.partner_id.cr
    #             self.cr_filename = self.partner_id.cr_filename
    #             self.tax_certificate = self.partner_id.tax_certificate
    #             self.tax_certificate_filename = self.partner_id.tax_certificate_filename
    #             self.national_address = self.partner_id.national_address
    #             self.national_address_filename = self.partner_id.national_address_filename

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

    def btn_print_bank_report(self):
        self.ensure_one()
        data = {'id': self.id,
                'model': 'sale.order'}

        report_name = 'attach_ext.report_sale_order_rajhi_bank_view'

        return self.env['ir.actions.report'].search(
            [('report_name', '=', report_name), ('report_type', '=', 'qweb-pdf')],
            limit=1).report_action(self, data=data, config=False)

    def test_reserve_auto(self):
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

    @api.model
    def create(self, vals):
        # return super(SaleOrder, self).create(vals).action_create_stock_reservation_direct()

        res = super(SaleOrder, self).create(vals)
        if res.auto_reservation == True:
            res.test_reserve_auto()
        # else:
        return res
