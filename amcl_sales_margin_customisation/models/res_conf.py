from odoo import api, fields, models
from ast import literal_eval
import logging

_logger = logging.getLogger(__name__)

from odoo import fields, models

class Company(models.Model):
    _inherit = 'res.company'

    global_margin = fields.Integer(string='Global Sale Margin (%)', default=0)

class ResConfig(models.TransientModel):
    _inherit = 'res.config.settings'

    global_margin = fields.Integer(related='company_id.global_margin', string='Global Sale Margin (%)',readonly=False)


# =======
# from odoo import api, fields, models
# from ast import literal_eval
# import logging
#
# _logger = logging.getLogger(__name__)
#
# from odoo import fields, models
#
# class Company(models.Model):
#     _inherit = 'res.company'
#
#     global_margin = fields.Integer(string='Global Sale Margin (%)', default=0)
#
# class ResConfig(models.TransientModel):
#     _inherit = 'res.config.settings'
#
#     global_margin = fields.Integer(related='company_id.global_margin', string='Global Sale Margin (%)',readonly=False)
#
#
# >>>>>>> Stashed changes
