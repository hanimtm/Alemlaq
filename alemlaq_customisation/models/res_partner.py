# -*- coding: utf-8 -*-

from odoo import fields, models, api, _



class ResPartner(models.Model):
    _inherit = 'res.partner'

    journal_id = fields.Many2one('account.journal', string='Journal')