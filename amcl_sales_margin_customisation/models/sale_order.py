# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import AccessError, UserError, ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def _get_default_property_global_margin(self):
        property_global_margin = self.env['global.margin'].sudo().search([], order='id ASC')
        return property_global_margin[0]

    list_price = fields.Float(
        'Sales Price', compute='_compute_sales_price',
        digits='Product Price',
        help="Price at which the product is sold to customers.",
    )
    property_global_margin = fields.Many2one(
        'global.margin', "Global Margin",
        company_dependent=True, check_company=True,
        domain="['|',('company_id', '=', False), ('company_id', '=', allowed_company_ids[0])]",
        default=_get_default_property_global_margin)

    margin_price = fields.Float(
        'Margin Price', compute='_compute_sales_price',
        digits='Product Price',
        help="Price at which the product is sold to customers.",
    )

    @api.depends('standard_price', 'property_global_margin')
    def _compute_sales_price(self):
        property_global_margin = False
        self.list_price = 0
        for product in self:
            if not product.property_global_margin:
                property_global_margin = self.env['global.margin'].sudo().search([], order='id ASC')[0]
            elif product.property_global_margin:
                property_global_margin = product.property_global_margin
            else:
                property_global_margin = False

            if property_global_margin:
                price = product.standard_price

                # --brand-- #
                brand = property_global_margin.brand.filtered(lambda l: l.name == str(product.brand).lower())
                if brand:
                    price = self.calculate_margin(brand, price)

                # --product_vc-- #
                product_vc = property_global_margin.product_vc.filtered(
                    lambda l: l.name == str(product.product_vc).lower())
                if product_vc:
                    price = self.calculate_margin(product_vc, price)

                # --year-- #
                year = property_global_margin.year.filtered(
                    lambda l: l.name == str(product.model_year).lower())
                if year:
                    price = self.calculate_margin(year, price)

                # --grade-- #
                grade = property_global_margin.grade.filtered(
                    lambda l: l.name == str(product.grade).lower())
                if grade:
                    price = self.calculate_margin(grade, price)

                # --exterior_color-- #
                exterior_color = property_global_margin.exterior_color.filtered(
                    lambda l: l.name == str(product.exterior_color).lower())
                if exterior_color:
                    price = self.calculate_margin(exterior_color, price)

                # --interior_color-- #
                interior_color = property_global_margin.interior_color.filtered(
                    lambda l: l.name == str(product.interior_color).lower())
                if interior_color:
                    price = self.calculate_margin(interior_color, price)

                # --transmission_type-- #
                transmission_type = property_global_margin.transmission_type.filtered(
                    lambda l: l.name == product.transmission_type)
                if transmission_type:
                    price = self.calculate_margin(transmission_type, price)

                product.list_price = price
                product.margin_price = price

    def calculate_margin(self, margin, price):
        if margin:
            if margin.type == 'percentage':
                price = price + ((price * margin.amount) / 100)
            else:
                price = price + margin.amount
            return price

    @api.constrains('list_price', 'margin_price')
    def _check_percent(self):
        for product in self:
            if product.list_price < product.margin_price:
                raise ValidationError(_('You can not change the Sale price less than Margin'))


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.onchange('sales_type_id')
    def _onchange_sales_type_id(self):
        for line in self.order_line:
            line.product_id_change()


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_id','order_id.sales_type_id')
    def product_id_change(self):
        res = super(SaleOrderLine, self).product_id_change()
        if self.product_id and (not self.product_id.property_global_margin or self.product_id.margin_price <= 0):
            raise ValidationError(_('Please configure the Global Margin and assign to Product.'))
        if self.order_id.sales_type_id:
            if not self.product_id.property_global_margin:
                property_global_margin = self.env['global.margin'].sudo().search([], order='id ASC')[0]
            elif self.product_id.property_global_margin:
                property_global_margin = self.product_id.property_global_margin
            else:
                raise ValidationError(_('Please configure the Global Margin and assign to Product.'))

            sales_type = property_global_margin.sales_type.filtered(
                    lambda l: l.id == self.order_id.sales_type_id.id)
            if sales_type:
                if sales_type.type == 'percentage':
                    self.price_unit = self.price_unit + ((self.price_unit * sales_type.amount) / 100)
                else:
                    self.price_unit = self.price_unit + sales_type.amount
        else:
            self.price_unit = self.product_id.margin_price
        return res

    @api.onchange('price_unit')
    def onchange_unit_price_change(self):
        margin = self.product_id.margin_price
        if margin > 0 and self.env.user.has_group(
                'sales_team.group_sale_salesman') and (
                not self.env.user.has_group('sales_team.group_sale_manager') or not self.env.user.has_group(
            'base.group_erp_manager')):
            if (self.price_unit != 0 and self.price_unit < margin) or (
                    self.price_unit != 0 and self.price_unit < self.product_id.standard_price):
                self.write({'price_unit': margin})
                raise UserError(
                    _('You can not enter a Unit Price, which is less than marginal amount or less than the cost.'))
