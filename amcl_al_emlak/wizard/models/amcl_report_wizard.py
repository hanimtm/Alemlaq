from odoo import fields, models, api
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)


class AMCLReportingWizard(models.TransientModel):
    _name = 'amcl.reporting.wizard'

    sale_order_id = fields.Many2one(comodel_name='sale.order', string='Sale Order')
    # sale_order_state = fields.Selection(related='sale_order_id.state')

    type_report = fields.Selection([('normal_confession', 'اقرار عادي'),
                                    ('form_receipt', 'نموذج استلام'),
                                    ('form_no_4_commitment_of_individuals', 'نموذج رقم 4 - تعهد الأفراد'),
                                    ('user_acknowledgment_form', 'نموذج إقرار المستخدم'),
                                    ('vehicle_registration_woman', 'إقرار بتسجيل مركبة بإسم إمرأة'),
                                    ('vehicle_registration_agency', 'إقرار تسجيل مركبة بوكالة'),
                                    ('vehicle_registration_authorization', 'تفويض بتسجيل مركبة')
                                    ],
                                   string='Chose Report Type', default='normal_confession')

    # catch_receipt = fields.Boolean(string='Catch Receipt', default=False)

    def get_line(self):
        line = self.env['sale.order.line'].search([('order_id', '=', self.sale_order_id.id)], limit=1)
        if line:
            arr = []
            dicfile = {
                'name': line.product_id.name,
                'qty': line.product_uom_qty,
                'model_year': line.product_id.model_year,
                'key_number': line.product_id.key_number,
                'vehicle_model': line.product_id.vehicle_model,
                'exterior_color': line.product_id.exterior_color,
                'haykal': line.product_id.default_code,
                'brand': line.product_id.brand,
                'card_no': line.product_id.card_no
            }
            arr.append(dicfile)
            return arr

    def button_print_report_ordinary_confession_pdf(self):
        self.ensure_one()
        data = {
            'id': self.id,
            'model': 'amcl.reporting.wizard',
        }
        report_type = 'qweb-pdf'
        report_name = ''

        # if self.catch_receipt:
        #     report_name += 'amcl_al_emlak.report_catch_receipt_report_view'

        if str(self.type_report) == "form_receipt":
            report_name += 'amcl_al_emlak.report_sale_order_receipt_form_view'

        elif self.type_report == 'normal_confession':
            report_name += 'amcl_al_emlak.report_sale_order_ordinary_confession_view'

        elif self.type_report == 'form_no_4_commitment_of_individuals':
            report_name += 'amcl_al_emlak.form_nb_4_commitment_of_individuals'

        elif self.type_report == 'user_acknowledgment_form':
            report_name += 'amcl_al_emlak.report_user_acknowledgment_form_view'

        elif self.type_report == 'vehicle_registration_woman':
            report_name += 'amcl_al_emlak.report_vehicle_registration_woman_view'

        elif self.type_report == 'vehicle_registration_agency':
            report_name += 'amcl_al_emlak.report_vehicle_registration_agency_view'

        elif self.type_report == 'vehicle_registration_authorization':
            report_name += 'amcl_al_emlak.report_vehicle_registration_authorization'

        else:
            raise ValidationError('الرجاء اختيار نوع التقرير المطلوب')

        return self.env['ir.actions.report'].search(
            [('report_name', '=', report_name),
             ('report_type', '=', report_type)], limit=1).report_action(self, data=data, config=False)

