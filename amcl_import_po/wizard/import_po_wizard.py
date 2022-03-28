# -*- coding: utf-8 -*-
# Part of AHCEC/VEICO.

import base64
import csv
from datetime import datetime

import xlrd
from odoo import fields, models, _
from odoo.exceptions import ValidationError, UserError
from odoo.tools import ustr
import uuid
import psycopg2


class ImportPoWizard(models.TransientModel):
    _name = 'import.po.wizard'
    _description = 'Import PO Wizard'

    count = 1

    import_type = fields.Selection([
        # ('csv', 'CSV File'),
        ('excel', 'Excel File')
    ], default="excel", string="Import File Type", required=True)
    file = fields.Binary(string="File", required=True)
    product_by = fields.Selection([
        ('name', 'Name'),
        ('int_ref', 'Internal Reference'),
        ('barcode', 'Barcode')
    ], default="name", string="Product By", required=True)
    is_create_vendor = fields.Boolean(string="Create Vendor?")
    is_confirm_order = fields.Boolean(string="Auto Confirm Order?")
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    branch_id = fields.Many2one('company.branch', string="Branch")
    product_categ_id = fields.Many2one('product.category', string='Product Category')
    sequence_id = fields.Char('Sequence', default=lambda self: str(uuid.uuid4()))

    order_no_type = fields.Selection([
        ('auto', 'Auto'),
        # ('as_per_sheet', 'As per sheet')
    ], default="auto", string="Reference Number", required=True)

    def show_success_msg_duplicate(self, existing_product_list):
        try:

            view = self.env.ref('amcl_import_po.ahcec_message_wizard')
            # view_id = view and view.id or False
            context = dict(self._context or {})
            dic_msg = "The below VIN is already available \n" + str(existing_product_list)
            context['message'] = dic_msg

            return {
                'name': 'Success',
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'import.message.wizard',
                'views': [(view.id, 'form')],
                'view_id': view.id,
                'target': 'new',
                'context': context,
            }
        except psycopg2.Error:
            pass

    def show_success_msg(self, counter, confirm_rec, skipped_line_no, existing_product_list, no_partner, already):

        view = self.env.ref('amcl_import_po.ahcec_message_wizard')
        # view_id = view and view.id or False
        context = dict(self._context or {})
        if counter == -1:
            if not no_partner:
                dic_msg = "No default vendor is set, Please ask the administrator to set."
            elif already:
                dic_msg = "Records imported successfully"
            else:
                dic_msg = "The below VIN is already available \n" + str(existing_product_list)
        elif len(skipped_line_no) >= 1:
            dic_msg = str(counter) + " Records not imported successfully \n"
            if skipped_line_no:
                dic_msg = dic_msg + "\nNote:"
            for k, v in skipped_line_no.items():
                dic_msg = dic_msg + "\nRow No " + k + " " + v + " "
        else:
            dic_msg = str(counter) + " Records imported successfully \n"
            dic_msg = dic_msg + str(confirm_rec) + " Records Confirm"
            if skipped_line_no:
                dic_msg = dic_msg + "\nNote:"
            for k, v in skipped_line_no.items():
                dic_msg = dic_msg + "\nRow No " + k + " " + v + " "
        context['message'] = dic_msg

        return {
            'name': 'Success',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'import.message.wizard',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context': context,
        }

    def import_po(self):
        self.ensure_one()
        counter = 1
        no_partner = True
        pol_obj = self.env['purchase.order.line']
        purchase_order_obj = self.env['purchase.order']
        product_product_obj = self.env['product.product']
        existing_product_list = []
        created_po_list_for_confirm = []
        created_po_list = []
        lines = []
        po_vals = {}
        skipped_line_no = {}

        for wizard in self:
            if wizard.import_type == 'excel':
                try:
                    wb = xlrd.open_workbook(file_contents=base64.decodestring(self.file))
                    sheet = wb.sheet_by_index(0)
                    for row in range(sheet.nrows):
                        search_product = product_product_obj.search(
                            [('default_code', '=', sheet.cell(row, 0).value or " ")])
                        if search_product:
                            existing_product_list.append(search_product.default_code or "")
                    if existing_product_list:
                        counter = -1
                        break
                    else:
                        skip_header = True
                        partner = self.env.company.default_vendor
                        print('Partner :: ', partner)
                        if not partner:
                            no_partner = False
                            counter == -1
                            break

                        for row in range(sheet.nrows):
                            try:
                                if skip_header:
                                    skip_header = False
                                    counter = counter + 1
                                    continue
                                vals = {}
                                search_product = product_product_obj.search(
                                    [('default_code', '=', sheet.cell(row, 0).value or " ")])

                                if not search_product:
                                    search_product = self.env['product.product'].sudo().create({
                                        'name': sheet.cell(row, 2).value,
                                        'type': 'product',
                                        'model_year': sheet.cell(row, 13).value,
                                        'grade': sheet.cell(row, 12).value,
                                        'default_code': str(sheet.cell(row, 0).value),
                                        'exterior_color_code': str(sheet.cell(row, 8).value),
                                        'exterior_color': str(sheet.cell(row, 9).value),
                                        'interior_color_code': str(sheet.cell(row, 10).value),
                                        'item': str(sheet.cell(row, 4).value),
                                        'interior_color': str(sheet.cell(row, 11).value),
                                        'alj_suffix': str(sheet.cell(row, 6).value),
                                        'vehicle_model': str(sheet.cell(row, 1).value),
                                        'brand': str(sheet.cell(row, 7).value),
                                        'standard_price': float(sheet.cell(row, 5).value),
                                        'sales_document': str(sheet.cell(row, 3).value),
                                        'company_id': self.company_id.id,
                                        'branch_id': self.branch_id.id,
                                        'categ_id': self.product_categ_id.id,
                                    })

                                if search_product:
                                    search_product.sudo().branch_id = self.branch_id.id
                                    print('Product :: ', str(sheet.cell(row, 3).value))
                                    search_product.sudo().barcode = str(sheet.cell(row, 0).value)
                                    lines.append((0, 0, {
                                        'product_id': search_product.id,
                                        'name': str(search_product.name),
                                        'product_qty': 1.0,
                                        'product_uom': search_product.uom_po_id.id,
                                        'price_unit': float(sheet.cell(row, 5).value),
                                        'date_planned': datetime.now(),
                                        'model_year': str(sheet.cell(row, 13).value),
                                        'grade': str(sheet.cell(row, 12).value),
                                        'exterior_color_code': str(sheet.cell(row, 8).value),
                                        'exterior_color': str(sheet.cell(row, 9).value),
                                        'interior_color_code': str(sheet.cell(row, 10).value),
                                        'interior_color': str(sheet.cell(row, 11).value),
                                        'alj_suffix': str(sheet.cell(row, 6).value),
                                        'vehicle_model': str(sheet.cell(row, 1).value),
                                        'brand': str(sheet.cell(row, 7).value),
                                        'sales_document': str(sheet.cell(row, 3).value),
                                        'item': str(sheet.cell(row, 4).value),
                                        # 'order_id': created_po.id,
                                        'company_id': self.company_id.id,
                                        'branch_id': self.branch_id.id
                                    }))

                                    # created_pol = pol_obj.create(vals)
                                    counter = counter + 1

                            except Exception as e:
                                skipped_line_no[str(counter)] = " - Value is not valid " + ustr(e)
                                counter = counter + 1
                                break
                except Exception as e:
                    raise UserError(_("Sorry, Your excel file does not match with our format " + ustr(e)))

        if counter == -1:
            created_po = self.env['purchase.order'].sudo().search(
                [('import_wizard_id', '=', self.sequence_id)])
            already = False
            if created_po:
                already = True
            res = self.show_success_msg(counter, False, False, existing_product_list, no_partner, already)
            return res
        elif counter > 1 and len(skipped_line_no) == 0:
            po_vals.update({'partner_id': partner.id,
                            'date_order': datetime.now(),
                            'date_planned': datetime.now(),
                            'branch_id': self.branch_id.id,
                            'import_wizard_id': self.sequence_id,
                            'order_line': lines
                            })
            po_vals.update({})
            already = self.env['purchase.order'].sudo().search(
                [('import_wizard_id', '=', self.sequence_id)])
            print('Already :: ', already)
            created_po = purchase_order_obj.sudo().create(po_vals)
            created_po_list_for_confirm.append(created_po.id)
            created_po_list.append(created_po.id)
            if created_po_list_for_confirm and self.is_confirm_order is True:
                purchase_orders = purchase_order_obj.search([('id', 'in', created_po_list_for_confirm)])
                if purchase_orders:
                    for purchase_order in purchase_orders:
                        purchase_order.button_confirm()
            else:
                created_po_list_for_confirm = []
            completed_records = len(created_po_list)
            confirm_rec = len(created_po_list_for_confirm)


            res = self.show_success_msg(created_po_list, confirm_rec, skipped_line_no, existing_product_list,
                                            no_partner,  False)
            return res
        else:
            res = self.show_success_msg(created_po_list, False, skipped_line_no, existing_product_list,
                                        no_partner, False)
            return res
