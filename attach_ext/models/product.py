from odoo import models


class Product(models.Model):
    _inherit = 'product.product'
    _order = 'create_date desc'


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    _order = 'create_date desc'

