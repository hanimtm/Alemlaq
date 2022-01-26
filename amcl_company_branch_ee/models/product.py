from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    branch_id = fields.Many2one('company.branch', string="Branch", required=True)


class ProductProduct(models.Model):
    _inherit = 'product.product'

    branch_id = fields.Many2one('company.branch', string="Branch", compute='_compute_branch_id', store=True)

    @api.depends('product_tmpl_id')
    def _compute_branch_id(self):
        if self.product_tmpl_id:
            self.branch_id = self.product_tmpl_id.branch_id.id