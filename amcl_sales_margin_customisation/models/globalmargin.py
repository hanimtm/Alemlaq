from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class GlobalMargin(models.Model):
    _name = 'global.margin'

    name = fields.Char('Name', required=True)
    global_margin = fields.Float(string='Global Sale Margin (%)', required=True, default=0)
    brand = fields.One2many('brand.margin', 'margin_id', 'Brand')
    product_vc = fields.One2many('product_vc.margin', 'margin_id', 'Product (VC)')
    year = fields.One2many('year.margin', 'margin_id', 'Year')
    grade = fields.One2many('grade.margin', 'margin_id', 'Grade')
    exterior_color = fields.One2many('exterior_color.margin', 'margin_id', 'Exterior Color')
    interior_color = fields.One2many('interior_color.margin', 'margin_id', 'Interior Color')
    transmission_type = fields.One2many('transmission_type.margin', 'margin_id', 'Transmission Type')
    sales_type = fields.One2many('sales_type.margin', 'margin_id', 'Sales Type')
    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)

    # @api.constrains('name')
    # def _check_pos_config(self):
    #     if self.search_count([]) > 1:
    #         raise ValidationError(_("You can not create more than one Global Margin"))


class BrandMargin(models.Model):
    _name = 'brand.margin'

    @api.model
    def _selection_brand(self):
        data = []
        for product in self.env['product.template'].sudo().search([('brand', '!=', False)]):
            if product.brand not in data:
                data.append(product.brand)
        return [(str(brand).lower(), brand) for brand in data]

    name = fields.Selection(string='Name', selection='_selection_brand')
    margin_id = fields.Many2one('global.margin', 'Global Margin')
    type = fields.Selection([('amount', 'Amount'),
                             ('percentage', 'Percentage')],
                            string="Type", default='amount')
    amount = fields.Float('Amount')


class YearMargin(models.Model):
    _name = 'year.margin'

    @api.model
    def _selection_year(self):
        data = []
        for product in self.env['product.template'].sudo().search([('model_year', '!=', False)]):
            if product.model_year not in data:
                data.append(product.model_year)
        return [(str(year).lower(), year) for year in data]

    name = fields.Selection(string='Name', selection='_selection_year')
    margin_id = fields.Many2one('global.margin', 'Global Margin')
    type = fields.Selection([('amount', 'Amount'),
                             ('percentage', 'Percentage')],
                            string="Type", default='amount')
    amount = fields.Float('Amount')


class ProductVcMargin(models.Model):
    _name = 'product_vc.margin'

    @api.model
    def _selection_product_vc(self):
        data = []
        for product in self.env['product.template'].sudo().search([('product_vc', '!=', False)]):
            if product.product_vc not in data:
                data.append(product.product_vc)
        return [(str(product_vc).lower(), product_vc) for product_vc in data]

    name = fields.Selection(string='Name', selection='_selection_product_vc')
    margin_id = fields.Many2one('global.margin', 'Global Margin')
    type = fields.Selection([('amount', 'Amount'),
                             ('percentage', 'Percentage')],
                            string="Type", default='amount')
    amount = fields.Float('Amount')

class GradeMargin(models.Model):
    _name = 'grade.margin'

    @api.model
    def _selection_grade(self):
        data = []
        for product in self.env['product.template'].sudo().search([('grade', '!=', False)]):
            if product.grade not in data:
                data.append(product.grade)
        return [(str(grade).lower(), grade) for grade in data]

    name = fields.Selection(string='Name', selection='_selection_grade')
    margin_id = fields.Many2one('global.margin', 'Global Margin')
    type = fields.Selection([('amount', 'Amount'),
                             ('percentage', 'Percentage')],
                            string="Type", default='amount')
    amount = fields.Float('Amount')


class ExteriorColorMargin(models.Model):
    _name = 'exterior_color.margin'

    @api.model
    def _selection_exterior_color(self):
        data = []
        for product in self.env['product.template'].sudo().search([('exterior_color', '!=', False)]):
            if product.exterior_color not in data:
                data.append(product.exterior_color)
        return [(str(exterior_color).lower(), exterior_color) for exterior_color in data]

    name = fields.Selection(string='Name', selection='_selection_exterior_color')
    margin_id = fields.Many2one('global.margin', 'Global Margin')
    type = fields.Selection([('amount', 'Amount'),
                             ('percentage', 'Percentage')],
                            string="Type", default='amount')
    amount = fields.Float('Amount')


class InteriorColorMargin(models.Model):
    _name = 'interior_color.margin'

    @api.model
    def _selection_interior_color(self):
        data = []
        for product in self.env['product.template'].sudo().search([('interior_color', '!=', False)]):
            if product.interior_color not in data:
                data.append(product.interior_color)
        return [(str(interior_color).lower(), interior_color) for interior_color in data]

    name = fields.Selection(string='Name', selection='_selection_interior_color')
    margin_id = fields.Many2one('global.margin', 'Global Margin')
    type = fields.Selection([('amount', 'Amount'),
                             ('percentage', 'Percentage')],
                            string="Type", default='amount')
    amount = fields.Float('Amount')


class TransmissionTypeMargin(models.Model):
    _name = 'transmission_type.margin'

    name = fields.Selection(
            [('automatic', 'AUTOMATIC'),
                ('cvt', 'CVT'),
                ('manual', 'MANUAL')], string="Name")
    margin_id = fields.Many2one('global.margin', 'Global Margin')
    type = fields.Selection([('amount', 'Amount'),
                             ('percentage', 'Percentage')],
                            string="Type", default='amount')
    amount = fields.Float('Amount')


class SalesTypeMargin(models.Model):
    _name = 'sales_type.margin'

    name = fields.Many2one('sale.type', string="Name")
    margin_id = fields.Many2one('global.margin', 'Global Margin')
    type = fields.Selection([('amount', 'Amount'),
                             ('percentage', 'Percentage')],
                            string="Type", default='amount')
    amount = fields.Float('Amount')