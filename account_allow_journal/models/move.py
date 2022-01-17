# -*- coding: utf-8 -*-
from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    suitable_journal_ids = fields.Many2many('account.journal', compute='_compute_suitable_journal_new_ids')

    @api.depends('company_id', 'invoice_filter_type_domain')
    def _compute_suitable_journal_new_ids(self):
        for m in self:
            company_id = m.company_id.id or self.env.company.id
            domain = [('company_id', '=', company_id)]
            m.suitable_journal_ids = self.env['account.journal'].search(domain)
