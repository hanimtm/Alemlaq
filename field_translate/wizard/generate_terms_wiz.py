# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class GenerateTermsWiz(models.TransientModel):
    _name = 'generate.terms.wiz'
    _description = "Generate Terms Wiz"

    field_name = fields.Selection(
        [('product.template,name', 'Product Name'), ('product.template,exterior_color_code', 'Exterior Color Code'),
         ('product.template,exterior_color', 'Exterior Color'),
         ('product.template,interior_color_code', 'Interior Color Code'),
         ('product.template,interior_color', 'Interior Color'), ('product.template,vehicle_model', 'Vehicle Model'),
         ('product.template,brand', 'Brand'), ('product.template,model_code', 'Model Code'),
         ('product.template,description', 'Description')], required=1)
    line_ids = fields.One2many('generate.terms.wiz.line', 'terms_id', 'Updatable Lines')

    @api.onchange('field_name')
    def onchange_field_name(self):
        """
        Onchange Field Name
        :return:
        """
        if self.field_name:
            print ('self.field_name', self.field_name)
            translation_lst = []
            src_lst = []
            for translation_rec in self.env['ir.translation'].search([
                ('lang', '=', 'ar_001'), ('name', '=', self.field_name)]):
                if translation_rec.src not in src_lst:
                    translation_lst.append(translation_rec)
                    src_lst.append(translation_rec.src)
                print ('translation_rec ---> ', translation_rec)
            print ('terms_lst ---> ', translation_lst)
            line_value = []
            for line_rec in self.line_ids:
                line_value.append((2, line_rec.id))
            for tr_rec in translation_lst:
                line_value.append((0, 0, {'translation_id': tr_rec.id, 'src': tr_rec.src, 'value': tr_rec.value}))
            self.line_ids = line_value

    def update_missing_product_terms(self):
        """
        Update Missing Term
        :return:
        """
        if self.line_ids:
            print ('self.line_ids -----> ', self.line_ids)
            for line in self.line_ids:
                line.translation_id.write({'value': line.value})


class GenerateTermsWizLine(models.TransientModel):
    _name = 'generate.terms.wiz.line'
    _description = "Generate Terms Wiz Line"

    translation_id = fields.Many2one('ir.translation', 'Translation')
    src = fields.Char('Internal Source')
    value = fields.Char('Translation Value')
    terms_id = fields.Many2one('generate.terms.wiz', 'Generate Terms Wiz')

    # def get_exist_term(self, res_id, lang, name, type):
    #     """
    #     get exist Terms
    #     :return:
    #     """
    #     name_terms = self.env['ir.translation'].search(
    #         [('res_id', '=', res_id), ('lang', '=', lang), ('name', '=', name),
    #          ('type', '=', type)])
    #     return name_terms
    #
    # def prepare_term_vals(self, product_rec, name):
    #     """
    #     Prepare translate vals
    #     :return:
    #     """
    #     translate_name = self.env['ir.translation'].search(
    #         [('src', '=', product_rec.name), ('value', '!=', ''), ('lang', '=', 'ar_001')], limit=1)
    #     return {
    #         'src': product_rec.name,
    #         'value': translate_name and translate_name.value or '',
    #         'name': 'product.template,name',
    #         'lang': 'ar_001',
    #         'type': 'model',
    #         'res_id': product_rec.id
    #     }
    #
    # def generate_missing_product_terms(self):
    #     """
    #     Generate Missing Product Terms
    #     :return:
    #     """
    #     for product in self.env['product.template'].search([]):
    #
    #         # name
    #         name_terms = self.get_exist_term(product.id, 'ar_001', 'product.template,name', 'model')
    #         if not name_terms:
    #             vals = self.prepare_term_vals(product, 'product.template,name')
    #             self.env['ir.translation'].sudo().create(vals)
    #
    #         # exterior_color_code
    #         exterior_color_code_terms = self.get_exist_term(
    #             product.id, 'ar_001', 'product.template,exterior_color_code', 'model')
    #         if not exterior_color_code_terms:
    #             vals = self.prepare_term_vals(product, 'product.template,exterior_color_code')
    #             self.env['ir.translation'].sudo().create(vals)
    #
    #         # exterior_color
    #         exterior_color_terms = self.get_exist_term(
    #             product.id, 'ar_001', 'product.template,exterior_color', 'model')
    #         if not exterior_color_terms:
    #             vals = self.prepare_term_vals(product, 'product.template,exterior_color')
    #             self.env['ir.translation'].sudo().create(vals)
    #
    #         # interior_color_code
    #         interior_color_code_terms = self.get_exist_term(
    #             product.id, 'ar_001', 'product.template,interior_color_code', 'model')
    #         if not interior_color_code_terms:
    #             vals = self.prepare_term_vals(product, 'product.template,interior_color_code')
    #             self.env['ir.translation'].sudo().create(vals)
    #
    #         # interior_color
    #         interior_color_terms = self.get_exist_term(
    #             product.id, 'ar_001', 'product.template,interior_color', 'model')
    #         if not interior_color_terms:
    #             vals = self.prepare_term_vals(product, 'product.template,interior_color')
    #             self.env['ir.translation'].sudo().create(vals)
    #
    #         # vehicle_model
    #         vehicle_model_terms = self.get_exist_term(
    #             product.id, 'ar_001', 'product.template,vehicle_model', 'model')
    #         if not vehicle_model_terms:
    #             vals = self.prepare_term_vals(product, 'product.template,vehicle_model')
    #             self.env['ir.translation'].sudo().create(vals)
    #
    #         # brand
    #         brand_terms = self.get_exist_term(
    #             product.id, 'ar_001', 'product.template,brand', 'model')
    #         if not brand_terms:
    #             vals = self.prepare_term_vals(product, 'product.template,brand')
    #             self.env['ir.translation'].sudo().create(vals)
    #
    #         # model_code
    #         model_code_terms = self.get_exist_term(
    #             product.id, 'ar_001', 'product.template,model_code', 'model')
    #         if not model_code_terms:
    #             vals = self.prepare_term_vals(product, 'product.template,model_code')
    #             self.env['ir.translation'].sudo().create(vals)
    #
    #         # description
    #         description_terms = self.get_exist_term(
    #             product.id, 'ar_001', 'product.template,description', 'model')
    #         if not description_terms:
    #             vals = self.prepare_term_vals(product, 'product.template,description')
    #             self.env['ir.translation'].sudo().create(vals)
