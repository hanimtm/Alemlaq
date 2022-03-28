from odoo import fields, models


class IrTranslate(models.Model):
    _inherit = 'ir.translation'

    show_in_catalog = fields.Boolean(string='Show In Catalog', default=False)
    product_id = fields.Many2one(comodel_name='product.template', string='Product')
    type_of_field = fields.Selection([
        ('name', 'Name'),
        ('exterior_color_code', 'Exterior Color Code'),
        ('exterior_color', 'Exterior Color'),
        ('interior_color_code', 'Interior Color Code'),
        ('interior_color', 'Interior Color'),
        ('vehicle', 'Vehicle'),
        ('brand', 'Brand'),
        ('model_code', 'Model Code'),
        ('description', 'Description')
    ], string='Type Of Field')

