from odoo import fields, models , api, _


class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    code = fields.Char('Short Name', required=True, size=250, help="Short name used to identify your warehouse")
    allowed_users = fields.Many2many('res.users', 'warehouse_user_rel', 'warehouse_id', 'user_id',
                                     string='Allowed Users')

    @api.onchange('branch_id')
    def _compute_allowed_users(self):
        if self and self.branch_id:
            self.allowed_users = self.branch_id.allowed_user_ids.ids
