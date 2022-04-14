from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # @api.model
    # def create(self, vals):
    #     res = super(ProductTemplate, self).create(vals)
    #     if 'name' in vals:
    #         translate_name = self.env['ir.translation'].search(
    #             [('src', '=', res.name), ('value', '!=', ''), ('lang', '=', 'ar_001')], limit=1)
    #
    #         self.env['ir.translation'].sudo().create({
    #             'src': vals['name'],
    #             'value': translate_name and translate_name.value or '',
    #             'name': 'product.template,name',
    #             'lang': 'ar_001',
    #             'type': 'model',
    #             'res_id': res.id
    #         })
    #     if 'exterior_color_code' in vals:
    #         translate_exterior_color_code = self.env['ir.translation'].search(
    #             [('src', '=', res.exterior_color_code), ('value', '!=', ''), ('lang', '=', 'ar_001')], limit=1)
    #         self.env['ir.translation'].sudo().create({
    #             'src': vals['exterior_color_code'],
    #             'value': translate_exterior_color_code and translate_exterior_color_code.value or '',
    #             'name': 'product.template,exterior_color_code',
    #             'lang': 'ar_001',
    #             'type': 'model',
    #             'res_id': res.id
    #         })
    #     if 'exterior_color' in vals:
    #         translate_exterior_color = self.env['ir.translation'].search(
    #             [('src', '=', res.exterior_color), ('value', '!=', ''), ('lang', '=', 'ar_001')], limit=1)
    #         self.env['ir.translation'].sudo().create({
    #             'src': vals['exterior_color'],
    #             'value': translate_exterior_color and translate_exterior_color.value or '',
    #             'name': 'product.template,exterior_color',
    #             'lang': 'ar_001',
    #             'type': 'model',
    #             'res_id': res.id
    #         })
    #     if 'interior_color_code' in vals:
    #         translate_interior_color_code = self.env['ir.translation'].search(
    #             [('src', '=', res.interior_color_code), ('value', '!=', ''), ('lang', '=', 'ar_001')], limit=1)
    #         self.env['ir.translation'].sudo().create({
    #             'src': vals['interior_color_code'],
    #             'value': translate_interior_color_code and translate_interior_color_code.value or '',
    #             'name': 'product.template,interior_color_code',
    #             'lang': 'ar_001',
    #             'type': 'model',
    #             'res_id': res.id
    #         })
    #     if 'interior_color' in vals:
    #         translate_interior_color = self.env['ir.translation'].search(
    #             [('src', '=', res.interior_color), ('value', '!=', ''), ('lang', '=', 'ar_001')], limit=1)
    #         self.env['ir.translation'].sudo().create({
    #             'src': vals['interior_color'],
    #             'value': translate_interior_color and translate_interior_color.value or '',
    #             'name': 'product.template,interior_color',
    #             'lang': 'ar_001',
    #             'type': 'model',
    #             'res_id': res.id
    #         })
    #     if 'vehicle_model' in vals:
    #         translate_vehicle = self.env['ir.translation'].search(
    #             [('src', '=', res.vehicle_model), ('value', '!=', ''), ('lang', '=', 'ar_001')], limit=1)
    #         self.env['ir.translation'].sudo().create({
    #             'src': vals['vehicle_model'],
    #             'value': translate_vehicle and translate_vehicle.value or '',
    #             'name': 'product.template,vehicle_model',
    #             'lang': 'ar_001',
    #             'type': 'model',
    #             'res_id': res.id
    #         })
    #     if 'brand' in vals:
    #         translate_brand = self.env['ir.translation'].search(
    #             [('src', '=', res.brand), ('value', '!=', ''), ('lang', '=', 'ar_001')], limit=1)
    #
    #         self.env['ir.translation'].sudo().create({
    #             'src': vals['brand'],
    #             'value': translate_brand and translate_brand.value or '',
    #             'name': 'product.template,brand',
    #             'lang': 'ar_001',
    #             'type': 'model',
    #             'res_id': res.id
    #         })
    #     if 'model_code' in vals:
    #         translate_model_code = self.env['ir.translation'].search(
    #             [('src', '=', res.model_code), ('value', '!=', ''), ('lang', '=', 'ar_001')], limit=1)
    #         self.env['ir.translation'].sudo().create({
    #             'src': vals['model_code'],
    #             'value': translate_model_code and translate_model_code.value or '',
    #             'name': 'product.template,model_code',
    #             'lang': 'ar_001',
    #             'type': 'model',
    #             'res_id': res.id
    #         })
    #     if 'description' in vals:
    #         if vals['description'] != '<p><br></p>':
    #             translate_model_code = self.env['ir.translation'].search(
    #                 [('src', '=', res.model_code), ('value', '!=', ''), ('lang', '=', 'ar_001')], limit=1)
    #             self.env['ir.translation'].sudo().create({
    #                 'src': vals['description'],
    #                 'value': translate_model_code and translate_model_code.value or '',
    #                 'name': 'product.template,description',
    #                 'lang': 'ar_001',
    #                 'type': 'model',
    #                 'res_id': res.id
    #             })
    #
    #     return res

    # def write(self, vals):
    #     for rec in self:
    #         if 'name' in vals:
    #             translate_name = self.env['ir.translation'].search(
    #                 [('type_of_field', '=', 'name'), ('product_id', '=', rec.id)])
    #             translate_name_search = self.env['ir.translation'].search(
    #                 [('src', '=', vals['name']), ('value', '!=', ''), ('type_of_field', '=', 'name')], limit=1)
    #             value = ''
    #             if translate_name_search:
    #                 value = translate_name_search.value
    #             translate_name.write({'src': vals['name'], 'value': value})
    #
    #         if 'exterior_color_code' in vals:
    #             translate_ext_color_code = self.env['ir.translation'].search(
    #                 [('type_of_field', '=', 'exterior_color_code'), ('product_id', '=', rec.id)])
    #             translate_exterior_color_code_search = self.env['ir.translation'].search(
    #                 [('src', '=', vals['exterior_color_code']), ('value', '!=', ''), ('type_of_field', '=', 'exterior_color_code')], limit=1)
    #             value = ''
    #             if translate_exterior_color_code_search:
    #                 value = translate_exterior_color_code_search.value
    #             translate_ext_color_code.write({'src': vals['exterior_color_code'], 'value': value})
    #
    #         if 'exterior_color' in vals:
    #             translate_ext_color = self.env['ir.translation'].search(
    #                 [('type_of_field', '=', 'exterior_color'), ('product_id', '=', rec.id)])
    #             translate_exterior_color_search = self.env['ir.translation'].search(
    #                 [('src', '=', vals['exterior_color']), ('value', '!=', ''), ('type_of_field', '=', 'exterior_color')], limit=1)
    #             value = ''
    #             if translate_exterior_color_search:
    #                 value = translate_exterior_color_search.value
    #             translate_ext_color.write({'src': vals['exterior_color'], 'value': value})
    #
    #         if 'interior_color_code' in vals:
    #             translate_int_color_code = self.env['ir.translation'].search(
    #                 [('type_of_field', '=', 'interior_color_code'), ('product_id', '=', rec.id)])
    #             translate_interior_color_code_search = self.env['ir.translation'].search(
    #                 [('src', '=', vals['interior_color_code']), ('value', '!=', ''), ('type_of_field', '=', 'interior_color_code')], limit=1)
    #             value = ''
    #             if translate_interior_color_code_search:
    #                 value = translate_interior_color_code_search.value
    #             translate_int_color_code.write({'src': vals['interior_color_code'], 'value': value})
    #
    #         if 'interior_color' in vals:
    #             translate_int_color = self.env['ir.translation'].search(
    #                 [('type_of_field', '=', 'interior_color'), ('product_id', '=', rec.id)])
    #             translate_interior_color_search = self.env['ir.translation'].search(
    #                 [('src', '=', vals['interior_color']), ('value', '!=', ''),
    #                  ('type_of_field', '=', 'interior_color')], limit=1)
    #             value = ''
    #             if translate_interior_color_search:
    #                 value = translate_interior_color_search.value
    #             translate_int_color.write({'src': vals['interior_color'], 'value': value})
    #
    #         if 'vehicle' in vals:
    #             translate_vehicle = self.env['ir.translation'].search(
    #                 [('type_of_field', '=', 'vehicle'), ('product_id', '=', rec.id)])
    #             translate_vehicle_search = self.env['ir.translation'].search(
    #                 [('src', '=', vals['vehicle']), ('value', '!=', ''),
    #                  ('type_of_field', '=', 'vehicle')], limit=1)
    #             value = ''
    #             if translate_vehicle_search:
    #                 value = translate_vehicle_search.value
    #             translate_vehicle.write({'src': vals['vehicle'], 'value': value})
    #
    #         if 'brand' in vals:
    #             translate_brand = self.env['ir.translation'].search(
    #                 [('type_of_field', '=', 'brand'), ('product_id', '=', rec.id)])
    #             translate_brand_search = self.env['ir.translation'].search(
    #                 [('src', '=', vals['brand']), ('value', '!=', ''),
    #                  ('type_of_field', '=', 'brand')], limit=1)
    #             value = ''
    #             if translate_brand_search:
    #                 value = translate_brand_search.value
    #             translate_brand.write({'src': vals['brand'], 'value': value})
    #
    #         if 'model_code' in vals:
    #             translate_model_code = self.env['ir.translation'].search(
    #                 [('type_of_field', '=', 'model_code'), ('product_id', '=', rec.id)])
    #             translate_model_code_search = self.env['ir.translation'].search(
    #                 [('src', '=', vals['model_code']), ('value', '!=', ''),
    #                  ('type_of_field', '=', 'model_code')], limit=1)
    #             value = ''
    #             if translate_model_code_search:
    #                 value = translate_model_code_search.value
    #             translate_model_code.write({'src': vals['model_code'], 'value': value})
    #
    #         if 'description' in vals:
    #             translate_model_code = self.env['ir.translation'].search(
    #                 [('type_of_field', '=', 'model_code'), ('product_id', '=', rec.id)])
    #             translate_description_search = self.env['ir.translation'].search(
    #                 [('src', '=', vals['description']), ('value', '!=', ''),
    #                  ('type_of_field', '=', 'description')], limit=1)
    #             value = ''
    #             if translate_description_search:
    #                 value = translate_description_search.value
    #             translate_model_code.write({'src': vals['description'], 'value': value})
    #
    #         return super(ProductTemplate, self).write(vals)

