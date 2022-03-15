from odoo import api, fields, models
from ast import literal_eval
import logging

_logger = logging.getLogger(__name__)


class ResConfig(models.TransientModel):
    _inherit = 'res.config.settings'

    nb_days = fields.Integer(string='Number Of Days', default=1)

    @api.model
    def get_values(self):
        res = super(ResConfig, self).get_values()

        ICPSudo = self.env['ir.config_parameter'].sudo()

        nb_days = literal_eval(ICPSudo.get_param('odoo_stock_reservation.nb_days', default='1'))

        res.update(nb_days=nb_days)
        return res

    def set_values(self):
        super(ResConfig, self).set_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        ICPSudo.set_param("odoo_stock_reservation.nb_days", self.nb_days)

