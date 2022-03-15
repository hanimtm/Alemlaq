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
        count = 1
        self.ensure_one()
        if self and self.file:
            self.ensure_one()
            pol_obj = self.env['purchase.order.line']
            purchase_order_obj = self.env['purchase.order']
            product_product_obj = self.env['product.product']
            existing_product_list = []
            count += 1
            # For Excel
            if self.import_type == 'excel':
                counter = 1
                skipped_line_no = {}
                try:
                    wb = xlrd.open_workbook(file_contents=base64.decodestring(self.file))
                    sheet = wb.sheet_by_index(0)
                    skip_header = True
                    running_po = None
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
                    created_po = self.env['purchase.order'].sudo().search(
                        [('import_wizard_id', '=', self.sequence_id)])
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
                                    [('default_code', '=', sheet.cell(row, 0).value)])
                                # if search_product:
                                #     existing_product_list.append(search_product.default_code or "")
                                #     break
                                #
                                # if existing_product_list:
                                #     raise UserError(_('Found existing Records %s.', existing_product_list))
                                try:
                                    if not search_product:
                                        search_product = self.env['product.product'].sudo().create({
                                            'name': sheet.cell(row, 2).value,
                                            'type': 'product',
                                            'model_year': sheet.cell(row, 13).value,
                                            'grade': sheet.cell(row, 12).value,
                                            'default_code': sheet.cell(row, 0).value,
                                            'barcode': sheet.cell(row, 0).value,
                                            'exterior_color_code': sheet.cell(row, 8).value,
                                            'exterior_color': sheet.cell(row, 9).value,
                                            'interior_color_code': sheet.cell(row, 10).value,
                                            'item': sheet.cell(row, 4).value,
                                            'interior_color': sheet.cell(row, 11).value,
                                            # 'transmission_type': type,
                                            # 'vms_customer': sheet.cell(row, 7).value,
                                            'alj_suffix': sheet.cell(row, 6).value,
                                            'vehicle_model': sheet.cell(row, 1).value,
                                            'brand': sheet.cell(row, 7).value,
                                            'standard_price': float(sheet.cell(row, 5).value),
                                            'sales_document': sheet.cell(row, 3).value,
                                            'company_id': self.company_id.id,
                                            'branch_id': self.branch_id.id,
                                            'categ_id': self.product_categ_id.id,
                                            # 'purchase_order': created_po.id,
                                        })
                                    if search_product:
                                        vals = {}
                                        print('Search product', search_product)
                                        search_product.product_tmpl_id.sudo().write({'branch_id': self.branch_id.id})
                                        created_pol = pol_obj.create({
                                            'product_id': search_product.id,
                                            'name': search_product.name,
                                            'product_qty': 1,
                                            'product_uom': search_product.uom_po_id.id,
                                            'price_unit': search_product.standard_price,
                                            'date_planned': datetime.now(),
                                            'model_year': search_product.model_year,
                                            'grade': search_product.grade,
                                            'exterior_color_code': search_product.exterior_color_code,
                                            'exterior_color': search_product.exterior_color,
                                            'interior_color_code': search_product.interior_color_code,
                                            'interior_color': search_product.interior_color,
                                            'alj_suffix': search_product.alj_suffix,
                                            'vehicle_model': search_product.vehicle_model,
                                            'brand': search_product.brand,
                                            'sales_document': search_product.sales_document,
                                            'item': search_product.item,
                                            'order_id': created_po.id,
                                            'company_id': self.company_id.id,
                                            'branch_id': self.branch_id.id
                                        })


                                        # search_product.sudo().branch_id = self.branch_id.id
                                        # search_product.product_tmpl_id.sudo().write({'branch_id': self.branch_id.id})
                                        # vals['product_id'] = search_product.id
                                        # vals['name'] = search_product.name
                                        # vals['product_qty'] = 1
                                        # vals['product_uom'] = search_product.uom_po_id.id
                                        # vals['price_unit'] = search_product.standard_price
                                        # vals['date_planned'] = datetime.now()
                                        # vals['model_year'] = search_product.model_year
                                        # vals['grade'] = search_product.grade
                                        # vals['exterior_color_code'] = search_product.exterior_color_code
                                        # vals['exterior_color'] = search_product.exterior_color
                                        # vals['interior_color_code'] = search_product.interior_color_code
                                        # vals['interior_color'] = search_product.interior_color
                                        # vals['alj_suffix'] = search_product.alj_suffix
                                        # vals['vehicle_model'] = search_product.vehicle_model
                                        # vals['brand'] = search_product.brand
                                        # vals['sales_document'] = search_product.sales_document
                                        # vals['item'] = search_product.item
                                        # vals['order_id'] = created_po.id
                                        # vals['company_id'] = self.company_id.id
                                        # vals['branch_id'] = self.branch_id.id
                                        # created_pol = pol_obj.create(vals)
                                        counter = counter + 1
                                        print('Line :', created_pol)
                                except Exception as e:
                                    raise UserError(_("Error :: ," + ustr(e)))
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

                if counter > 1:
                    completed_records = len(created_po_list)
                    confirm_rec = len(created_po_list_for_confirm)
                    res = self.show_success_msg(completed_records, confirm_rec, skipped_line_no)
                    return res
                    return True
