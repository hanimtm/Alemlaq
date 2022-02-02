# -*- coding: utf-8 -*-

from odoo import fields, models, _


class ImportMessage(models.TransientModel):
    _name = 'import.message.wizard'
    _description = 'Import Message Wizard'

    def get_default(self):
        if self.env.context.get("message", False):
            return self.env.context.get("message")
        return False

    name = fields.Text(string="Message", readonly=True, default=get_default)

    def action_open_purchase_orders(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
