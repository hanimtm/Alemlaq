# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from itertools import groupby
from odoo.tools.float_utils import float_compare
from odoo.tools import float_compare, float_is_zero
from collections import defaultdict
from odoo.exceptions import AccessError, UserError
from odoo.tools import format_date
from odoo.tools.misc import formatLang, format_date, get_lang
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_customer = fields.Boolean('Is Customer', compute='_compute_is_customer', readonly=False, store=True)
    is_vendor = fields.Boolean('Is Vendor', compute='_compute_is_vendor', readonly=False, store=True)
    is_employee = fields.Boolean('Is Employee', compute='_compute_is_employee', readonly=False, store=True)

    @api.depends()
    def _compute_is_customer(self):
        for partner in self:
            if partner.customer_rank > 0 or partner.total_invoiced > 0:
                partner.is_customer = True

    @api.depends()
    def _compute_is_vendor(self):
        for partner in self:
            if partner.supplier_rank > 0 or partner.supplier_invoice_count > 0:
                partner.is_vendor = True

    @api.depends()
    def _compute_is_employee(self):
        for partner in self:
            print('Employee Partner :: ', self.env['hr.employee'].search([('address_home_id', '=', partner.id)]))
            if self.env['hr.employee'].search([('address_home_id', '=', partner.id)]):
                partner.is_employee = True
