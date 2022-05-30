from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
import logging
_logger = logging.getLogger(__name__)


class AbstractBankReport(models.AbstractModel):
    _name = 'report.offer_price.report_sale_order_rajhi_bank_view'

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


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    license_plate_ids = fields.One2many('license.plate', 'sale_order_id', string='License Plate')

    insurance_text = fields.Char('الضمان بإسم')
    price_inc_license = fields.Char('السعر يشمل')

    def btn_open_wizard_create_new_license_plate(self):
        self.ensure_one()
        res = {
            'type': 'ir.actions.act_window',
            'name': _('Create New License Plate'),
            'res_model': 'license.plate.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            # 'view_id': view_id,
            'view_id': self.env.ref("offer_price.license_plate_wizard_view_form").id,
            'target': 'new',
            'context': {
                'default_sale_order_id': self.id
            }
        }
        return res

    def btn_print_bank_report(self):
        self.ensure_one()
        data = {'id': self.id,
                'model': 'sale.order'}

        report_name = 'offer_price.report_sale_order_rajhi_bank_view'

        return self.env['ir.actions.report'].search(
            [('report_name', '=', report_name), ('report_type', '=', 'qweb-pdf')],
            limit=1).report_action(self, data=data, config=False)

# class SaleOrderLine(models.Model):
#     _inherit = 'sale.order.line'
#
#     price_after_tax = fields.Float(compute='_compute_price_after_taxes', store=True)
#
#     @api.depends('tax_id')
#     def _compute_price_after_taxes(self):
#         for line in self:
#             line.price_after_tax = 0
#             for tax in line.tax_id:
#                 # raise ValidationError(str(tax.amount))
#                 line.price_after_tax += tax.amount
