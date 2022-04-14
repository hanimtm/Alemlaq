from odoo import api, fields, models
# import logging
# _logger = logging.getLogger(__name__)


class StockQuant(models.Model):
    _inherit = 'stock.quant'
    _description = 'Add related field from product'

    # product_name = fields.Char(related='product_id.product_tmpl_id.name')
    product_default_code = fields.Char(related='product_id.product_tmpl_id.default_code', store=1)
    product_brand = fields.Char(related='product_id.product_tmpl_id.brand', store=1)
    product_model_year = fields.Char(related='product_id.product_tmpl_id.model_year', store=1)
    product_ext_color_code = fields.Char(related='product_id.product_tmpl_id.exterior_color_code', store=1)
    product_int_color_code = fields.Char(related='product_id.product_tmpl_id.interior_color_code', store=1)
    product_ext_color = fields.Char(related='product_id.product_tmpl_id.exterior_color', store=1)
    product_int_color = fields.Char(related='product_id.product_tmpl_id.exterior_color', store=1)
    product_grade = fields.Char(related='product_id.product_tmpl_id.grade', store=1)
    product_key_number = fields.Char(related='product_id.product_tmpl_id.key_number', store=1)
    product_vessel_no = fields.Char(related='product_id.product_tmpl_id.vessel_no', store=1)
    product_card_no = fields.Char(related='product_id.product_tmpl_id.card_no', store=1)
    product_alj_suffix = fields.Char(related='product_id.product_tmpl_id.alj_suffix', store=1)
    product_vehicle_model = fields.Char(related='product_id.product_tmpl_id.vehicle_model', store=1)
