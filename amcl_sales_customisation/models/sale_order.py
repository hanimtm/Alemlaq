# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # mobile_no = fields.Char(string='Mobile No', related='partner_id.mobile')
    #e_mail = fields.Char(string='E-mail', related='partner_id.email')
    e_mail = fields.Many2one('res.partner',string='E-mail')
    mobile_no = fields.Many2one('res.partner', string='Mobile No')
    sales_type_id = fields.Many2one('sale.type', string='Sales Type')

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        res = super(SaleOrder, self).onchange_partner_id()
        if self.partner_id.sales_type_id:
            self.sales_type_id = self.partner_id.sales_type_id
        return res

    @api.onchange('mobile_no')
    def onchange_mobile_no(self):
        for each in self:
            if each.mobile_no:
                each.partner_id = each.mobile_no

    @api.onchange('e_mail')
    def onchange_e_mail(self):
        for each in self:
            if each.e_mail:
                each.partner_id = each.e_mail

    def read(self, records):
        res = super(SaleOrder, self).read(records)
        for each in res:
            if each.get('mobile_no'):
                each['mobile_no'] = (each.get('mobile_no')[0],self.env['res.partner'].browse(each.get('mobile_no')[0]).mobile)
            if each.get('e_mail'):
                each['e_mail'] = (
                each.get('e_mail')[0], self.env['res.partner'].browse(each.get('e_mail')[0]).email)
        return res

    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals['sale_order'] = self.id
        return invoice_vals

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _prepare_invoice_line(self, **optional_values):
        values = super(SaleOrderLine, self)._prepare_invoice_line(**optional_values)
        values['account_id'] = self.order_id.sales_type_id.income_account.id or False

        return values