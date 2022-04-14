# -*- coding: utf-8 -*-
# from odoo import models, fields, exceptions, api, _
from odoo import api, fields, models, _


class GenerateTermsWiz(models.TransientModel):
    _name = 'generate.terms.wiz'
    _description = "Generate Terms Wiz"

    def get_exist_term(self, res_id, lang, name, type):
        """
        get exist Terms
        :return:
        """
        name_terms = self.env['ir.translation'].search(
            [('res_id', '=', res_id), ('lang', '=', lang), ('name', '=', name),
             ('type', '=', type)])
        return name_terms

    def prepare_term_vals(self, product_rec, name):
        """
        Prepare translate vals
        :return:
        """
        translate_name = self.env['ir.translation'].search(
            [('src', '=', product_rec.name), ('value', '!=', ''), ('lang', '=', 'ar_001')], limit=1)
        return {
            'src': product_rec.name,
            'value': translate_name and translate_name.value or '',
            'name': 'product.template,name',
            'lang': 'ar_001',
            'type': 'model',
            'res_id': product_rec.id
        }

    def generate_missing_product_terms(self):
        """
        Generate Missing Product Terms
        :return:
        """
        for product in self.env['product.template'].search([]):

            # name
            name_terms = self.get_exist_term(product.id, 'ar_001', 'product.template,name', 'model')
            if not name_terms:
                vals = self.prepare_term_vals(product, 'product.template,name')
                self.env['ir.translation'].sudo().create(vals)

            # exterior_color_code
            exterior_color_code_terms = self.get_exist_term(
                product.id, 'ar_001', 'product.template,exterior_color_code', 'model')
            if not exterior_color_code_terms:
                vals = self.prepare_term_vals(product, 'product.template,exterior_color_code')
                self.env['ir.translation'].sudo().create(vals)

            # exterior_color
            exterior_color_terms = self.get_exist_term(
                product.id, 'ar_001', 'product.template,exterior_color', 'model')
            if not exterior_color_terms:
                vals = self.prepare_term_vals(product, 'product.template,exterior_color')
                self.env['ir.translation'].sudo().create(vals)

            # interior_color_code
            interior_color_code_terms = self.get_exist_term(
                product.id, 'ar_001', 'product.template,interior_color_code', 'model')
            if not interior_color_code_terms:
                vals = self.prepare_term_vals(product, 'product.template,interior_color_code')
                self.env['ir.translation'].sudo().create(vals)

            # interior_color
            interior_color_terms = self.get_exist_term(
                product.id, 'ar_001', 'product.template,interior_color', 'model')
            if not interior_color_terms:
                vals = self.prepare_term_vals(product, 'product.template,interior_color')
                self.env['ir.translation'].sudo().create(vals)

            # vehicle_model
            vehicle_model_terms = self.get_exist_term(
                product.id, 'ar_001', 'product.template,vehicle_model', 'model')
            if not vehicle_model_terms:
                vals = self.prepare_term_vals(product, 'product.template,vehicle_model')
                self.env['ir.translation'].sudo().create(vals)

            # brand
            brand_terms = self.get_exist_term(
                product.id, 'ar_001', 'product.template,brand', 'model')
            if not brand_terms:
                vals = self.prepare_term_vals(product, 'product.template,brand')
                self.env['ir.translation'].sudo().create(vals)

            # model_code
            model_code_terms = self.get_exist_term(
                product.id, 'ar_001', 'product.template,model_code', 'model')
            if not model_code_terms:
                vals = self.prepare_term_vals(product, 'product.template,model_code')
                self.env['ir.translation'].sudo().create(vals)

            # description
            description_terms = self.get_exist_term(
                product.id, 'ar_001', 'product.template,description', 'model')
            if not description_terms:
                vals = self.prepare_term_vals(product, 'product.template,description')
                self.env['ir.translation'].sudo().create(vals)
