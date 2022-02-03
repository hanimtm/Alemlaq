# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class CustomCardRequest(models.Model):
    _name = 'custom.card.request'
    _description = 'Custom Card Request'

    name = fields.Char(string='Request Number')
    partner_id = fields.Many2one('res.partner', string='Customer')
    user_id = fields.Many2one('res.users', string='Sales Person')
    sale_order_id = fields.Many2one('sale.order', string='Order')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('upload', 'Uploaded')
    ], default="draft", string="Status", required=True)

    is_record_uploaded = fields.Boolean(string='Is Record Uploaded?', default=False, copy=False)
    custom_card_request_ids = fields.One2many('custom.card.request.line','custom_card_request_id', string='Custom Card Request Ids')

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'custom.card.request') or 'New'
        result = super(CustomCardRequest, self).create(vals)
        return result

    def refuse_custom_card_request(self):
        self.write({'is_record_uploaded': False,'state': 'draft'})
        return True

    def process_custom_card_request(self):
        self.write({'is_record_uploaded': True,'state':'upload'})
        self.sale_order_id.sudo().write({'is_card_request_approved': True})
        return True

class CustomCardRequestLine(models.Model):
    _name = 'custom.card.request.line'
    _description = 'Custom Card Request Line'

    custom_card_request_id = fields.Many2one('custom.card.request', string='Request No')
    product_id = fields.Many2one('product.product')
    vin = fields.Char(string='VIN')
    upload_card = fields.Binary('Custom Card', attachment=True)
    custom_card_file = fields.Char()
