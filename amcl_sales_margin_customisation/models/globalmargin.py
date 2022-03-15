from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class GlobalMargin(models.Model):
    _name = 'global.margin'

    name = fields.Char('Name', required=True)
    global_margin = fields.Float(string='Global Sale Margin (%)', required=True, default=0)

    @api.constrains('name')
    def _check_pos_config(self):
        if self.search_count([]) > 1:
            raise ValidationError(_("You can not create more than one Global Margin"))

# class ResConfig(models.TransientModel):
#     _inherit = 'res.config.settings'
#
#     global_margin = fields.Integer(related='company_id.global_margin', string='Global Sale Margin (%)',readonly=False)
