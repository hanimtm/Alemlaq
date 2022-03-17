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


    def show_success_msg(self, counter, confirm_rec, skipped_line_no):

        # action = self.env.ref('amcl_import_po.import_po_action').sudo().read()[0]
        # action = {'type': 'ir.actions.act_window_close'}
        # open the new success message box
        try:
            view = self.env.ref('amcl_import_po.ahcec_message_wizard')
            # view_id = view and view.id or False
            context = dict(self._context or {})
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
        except psycopg2.Error:
            pass

    def import_po_apply(self):
        created_po = self.env['purchase.order'].sudo().search(
            [('import_wizard_id', '=', self.sequence_id)])
        if self and self.file and not created_po:
            self.ensure_one()
            pol_obj = self.env['purchase.order.line']
            purchase_order_obj = self.env['purchase.order']
            product_product_obj = self.env['product.product']
            existing_product_list = []
            # For Excel
            created_po = self.env['purchase.order'].sudo().search(
                [('import_wizard_id', '=', self.sequence_id)])
            if self.import_type == 'excel':
                counter = 1
                skipped_line_no = {}
                wb = xlrd.open_workbook(file_contents=base64.decodestring(self.file))
                sheet = wb.sheet_by_index(0)
                if not created_po:
                    for row in range(sheet.nrows):
                        search_product = product_product_obj.search(
                            [('default_code', '=', sheet.cell(row, 0).value or " ")])
                        if search_product:
                            existing_product_list.append(search_product.default_code or "")
                if existing_product_list:
                    counter = -1
                else:
                    try:
                        skip_header = True
                        created_po = False
                        created_po_list_for_confirm = []
                        created_po_list = []
                        partner = self.env.company.default_vendor
                        po_vals = {}
                        if not partner:
                            raise ValueError("Please add the Default Vendor in Settings")
                        po_vals.update({'partner_id': partner.id})
                        po_vals.update({'date_order': datetime.now()})
                        po_vals.update({'date_planned': datetime.now()})
                        po_vals.update({'branch_id': self.branch_id.id})
                        po_vals.update({'import_wizard_id': self.sequence_id})

                        if not created_po:
                            created_po = purchase_order_obj.sudo().create(po_vals)
                        created_po_list_for_confirm.append(created_po.id)
                        created_po_list.append(created_po.id)

                        for row in range(sheet.nrows):
                            try:
                                if skip_header:
                                    skip_header = False
                                    counter = counter + 1
                                    continue
                                if created_po:
                                    vals = {}
                                    type = False
                                    if sheet.cell(row, 6).value == 'AUTOMATIC':
                                        type = 'automatic'
                                    elif sheet.cell(row, 6).value == 'CVT':
                                        type = 'cvt'
                                    else:
                                        type = 'manual'

                                    search_product = product_product_obj.search(
                                        [('default_code', '=', sheet.cell(row, 0).value or " ")])

                                    try:
                                        if not search_product:
                                            search_product = self.env['product.product'].sudo().create({
                                                'name': sheet.cell(row, 2).value,
                                                'type': 'product',
                                                'model_year': sheet.cell(row, 13).value,
                                                'grade': sheet.cell(row, 12).value,
                                                'default_code': str(sheet.cell(row, 0).value),
                                                # 'barcode': str(sheet.cell(row, 0).value),
                                                'exterior_color_code': str(sheet.cell(row, 8).value),
                                                'exterior_color': str(sheet.cell(row, 9).value),
                                                'interior_color_code': str(sheet.cell(row, 10).value),
                                                'item': str(sheet.cell(row, 4).value),
                                                'interior_color': str(sheet.cell(row, 11).value),
                                                # 'transmission_type': type,
                                                # 'vms_customer': sheet.cell(row, 7).value,
                                                'alj_suffix': str(sheet.cell(row, 6).value),
                                                'vehicle_model': str(sheet.cell(row, 1).value),
                                                'brand': str(sheet.cell(row, 7).value),
                                                'standard_price': float(sheet.cell(row, 5).value),
                                                'sales_document': str(sheet.cell(row, 3).value),
                                                'company_id': self.company_id.id,
                                                'branch_id': self.branch_id.id,
                                                'categ_id': self.product_categ_id.id,
                                                # 'purchase_order': created_po.id,
                                            })
                                            print('No search product')
                                    except psycopg2.Error as e:
                                        print(str(e))
                                    if search_product:
                                        search_product.sudo().branch_id = self.branch_id.id

                                        # search_product.product_tmpl_id.sudo().write({'branch_id': self.branch_id.id})
                                        # print(search_product.product_tmpl_id)
                                        search_product.sudo().barcode = str(sheet.cell(row, 0).value)
                                        vals.update({'product_id': search_product.id})
                                        vals.update({'name': str(search_product.name)})
                                        vals.update({'product_qty': 1.0})
                                        vals.update({'product_uom': search_product.uom_po_id.id})
                                        vals.update({'price_unit': float(sheet.cell(row, 5).value)})
                                        vals.update({'date_planned': datetime.now()})
                                        vals.update({'model_year': str(sheet.cell(row, 13).value)})
                                        vals.update({'grade': str(sheet.cell(row, 12).value)})
                                        vals.update({'exterior_color_code': str(sheet.cell(row, 8).value)})
                                        vals.update({'exterior_color': str(sheet.cell(row, 9).value)})
                                        vals.update({'interior_color_code': str(sheet.cell(row, 10).value)})
                                        vals.update({'interior_color': str(sheet.cell(row, 11).value)})
                                        vals.update({'alj_suffix': str(sheet.cell(row, 6).value)})
                                        vals.update({'vehicle_model': str(sheet.cell(row, 1).value)})
                                        vals.update({'brand': str(sheet.cell(row, 7).value)})
                                        vals.update({'sales_document': str(sheet.cell(row, 3).value)})
                                        vals.update({'item': str(sheet.cell(row, 4).value)})
                                        vals.update({'order_id': created_po.id})
                                        vals.update({'company_id': self.company_id.id}),
                                        vals.update({'branch_id': self.branch_id.id}),
                                        created_pol = pol_obj.create(vals)
                                        counter = counter + 1
                                else:
                                    skipped_line_no[str(counter)] = " - Purchase Order not created. "
                                    counter = counter + 1
                                    continue

                            except Exception as e:
                                skipped_line_no[str(counter)] = " - Value is not valid " + ustr(e)
                                counter = counter + 1
                                continue
                        if created_po_list_for_confirm and self.is_confirm_order is True:
                            purchase_orders = purchase_order_obj.search([('id', 'in', created_po_list_for_confirm)])
                            if purchase_orders:
                                for purchase_order in purchase_orders:
                                    purchase_order.button_confirm()
                        else:
                            created_po_list_for_confirm = []

                    except Exception as e:
                        raise UserError(_("Sorry, Your excel file does not match with our format " + ustr(e)))
                if counter == -1:
                    res = self.show_success_msg_duplicate(existing_product_list)
                    return res

                if counter > 1:
                    completed_records = len(created_po_list)
                    confirm_rec = len(created_po_list_for_confirm)
                    res = self.show_success_msg(completed_records, confirm_rec, skipped_line_no)
                    return res
