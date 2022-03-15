from odoo import models, fields, api, _


class AMCLSaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    def btn_show_wizard_print(self):
        self.ensure_one()
        # view_ref = self.env['ir.model.data'].get_object_reference(
        #     'amcl_al_emlak',
        #     'amcl_report_wizard_view_form')
        # view_id = view_ref[1] if view_ref else False

        res = {
            'type': 'ir.actions.act_window',
            'name': _('Report'),
            'res_model': 'amcl.reporting.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            # 'view_id': view_id,
            'view_id': self.env.ref("amcl_al_emlak.amcl_report_wizard_view_form").id,
            'target': 'new',
            'context': {
                'default_sale_order_id': self.id
            }
        }
        return res
