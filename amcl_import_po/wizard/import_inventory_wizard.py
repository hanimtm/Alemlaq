# -*- coding: utf-8 -*-
# Part of AHCEC/VEICO.

import base64
import csv
from datetime import datetime

import xlrd
from odoo import fields, models, _
from odoo.exceptions import UserError
from odoo.tools import ustr


class ImportPoWizard(models.TransientModel):
    _name = 'import.inventory.wizard'
    _description = 'Import Inventory Wizard'

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

    def show_success_msg(self, counter, skipped_line_no):

        action = self.env.ref('amcl_import_po.import_po_action').read()[0]
        action = {'type': 'ir.actions.act_window_close'}

        # open the new success message box
        view = self.env.ref('amcl_import_po.ahcec_message_wizard')
        view_id = view and view.id or False
        context = dict(self._context or {})
        dic_msg = str(counter) + " Records imported successfully \n"
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

    def import_po_apply(self):
        picking = self.env['stock.picking'].browse(self.env.context['picking_id'])
        not_found_records = []
        if self and self.file:
            # For Excel
            if self.import_type == 'excel':
                counter = 1
                skipped_line_no = {}
                try:
                    wb = xlrd.open_workbook(file_contents=base64.decodestring(self.file))
                    sheet = wb.sheet_by_index(0)
                    skip_header = True
                    created_po_list = []

                    for row in range(sheet.nrows):
                        try:
                            if skip_header:
                                skip_header = False
                                counter = counter + 1
                                continue

                            if picking.move_lines:

                                move = picking.move_lines.filtered(
                                    lambda p: p.product_id.default_code == sheet.cell(row, 3).value.strip('\n'))

                                if not move:
                                    not_found_records.append(sheet.cell(row, 3).value)
                                    continue

                                if not_found_records:
                                    raise UserError(_('Not Found the Record %s.', not_found_records))

                                if move:
                                    vals = {}

                                    type = False
                                    if sheet.cell(row, 12).value == 'AUTOMATIC':
                                        type = 'automatic'
                                    elif sheet.cell(row, 12).value == 'CVT':
                                        type = 'cvt'
                                    else:
                                        type = 'manual'

                                    declaration_date = False
                                    if sheet.cell(row, 14).value not in (None, "", 0, 0.0):
                                        declaration_date = str(
                                            datetime.strptime(str(int(sheet.cell(row, 14).value)), '%Y%m%d').date())

                                    bill_date = False
                                    if sheet.cell(row, 16).value not in (None, "", 0, 0.0):
                                        bill_date = str(
                                            datetime.strptime(str(int(sheet.cell(row, 14).value)), '%Y%m%d').date())

                                    broker_declaration_date = False
                                    if sheet.cell(row, 18).value not in (None, "", 0, 0.0):
                                        broker_declaration_date = str(
                                            datetime.strptime(str(int(sheet.cell(row, 18).value)), '%Y%m%d').date())

                                    request_delivery_date = False
                                    if sheet.cell(row, 19).value not in (None, "", 0, 0.0):
                                        request_delivery_date = str(
                                            datetime.strptime(str(int(sheet.cell(row, 19).value)), '%Y%m%d').date())

                                    search_product = self.env['stock.receipt.line'].search([('picking_id','=',picking.id),('vin','=',sheet.cell(row, 3).value.strip('\n'))])
                                    if search_product:
                                        search_product = self.update_receipt_line_data(search_product)
                                        created_po_list.append(search_product.id)
                                        counter = counter + 1
                                    # if not search_product:
                                    #     search_product = self.env['stock.receipt.line'].create({
                                    #         'picking_id': picking.id,
                                    #         'brand': sheet.cell(row, 0).value,
                                    #         'product_id': move.product_id.id,
                                    #         'description': sheet.cell(row, 2).value,
                                    #         'vin': sheet.cell(row, 3).value,
                                    #         'exterior_color': str(int(sheet.cell(row, 4).value)) if isinstance(
                                    #             sheet.cell(row, 4).value, (float, int)) else sheet.cell(row, 4).value,
                                    #         'interior_color': str(int(sheet.cell(row, 5).value)) if isinstance(
                                    #             sheet.cell(row, 5).value, (float, int)) else sheet.cell(row, 5).value,
                                    #         'complete_engine_number': sheet.cell(row, 6).value,
                                    #         'model_code': sheet.cell(row, 7).value,
                                    #         'action': sheet.cell(row, 8).value,
                                    #         'alj_suffix': sheet.cell(row, 9).value,
                                    #         'model_year': str(int(sheet.cell(row, 10).value)) if isinstance(
                                    #             sheet.cell(row, 10).value, (float, int)) else sheet.cell(row, 10).value,
                                    #         'grade': sheet.cell(row, 11).value,
                                    #         'transmission_type': type,
                                    #         'sales_document': str(int(sheet.cell(row, 13).value)) if isinstance(
                                    #             sheet.cell(row, 13).value, (float, int)) else sheet.cell(row, 13).value,
                                    #         'request_delivery_date': request_delivery_date,
                                    #         'billing_document': str(int(sheet.cell(row, 15).value)) if isinstance(
                                    #             sheet.cell(row, 15).value, (float, int)) else sheet.cell(row, 15).value,
                                    #         'bill_date': bill_date,
                                    #         'vehicle_wholesale_price': sheet.cell(row, 17).value,
                                    #         'broker_declaration_date': broker_declaration_date,
                                    #         'declaration_date': declaration_date,
                                    #         'netval': sheet.cell(row, 20).value,
                                    #         'vat_amount': sheet.cell(row, 21).value,
                                    #     })
                                    #     created_po_list.append(search_product.id)
                                    #     counter = counter + 1
                                    # else:
                                    #     self.update_receipt_line_data(search_product)
                            else:
                                skipped_line_no[str(counter)] = " - Move not created. "
                                counter = counter + 1
                                continue

                        except Exception as e:
                            skipped_line_no[str(counter)] = " - Value is not valid " + ustr(e)
                            counter = counter + 1
                            continue

                except Exception as e:
                    raise UserError(_("Sorry, Your excel file does not match with our format " + ustr(e)))

                if counter > 1:
                    completed_records = len(created_po_list)
                    res = self.show_success_msg(completed_records, skipped_line_no)
                    picking.write({'product_imported': True})
                    return res


    def update_receipt_line_data(self,search_product):
        search_product.write({
            'picking_id': search_product.picking_id.id,
            'brand': search_product.product_id.brand or " ",
            'product_id': search_product.product_id.id,
            'description': search_product.product_id.description or " ",
            'vin': search_product.product_id.default_code or "",
            'exterior_color': search_product.product_id.exterior_color or " ",
            'interior_color': search_product.product_id.interior_color or "",
            'complete_engine_number': search_product.product_id.complete_engine_number or "",
            'model_code': search_product.product_id.model_code or "",
            'action': search_product.product_id.action or "",
            'alj_suffix': search_product.product_id.alj_suffix or "",
            'model_year': search_product.product_id.model_year or "",
            'grade': search_product.product_id.grade or "",
            'transmission_type': search_product.product_id.transmission_type or "",
            'sales_document':search_product.product_id.sales_document or "",
            'request_delivery_date': search_product.product_id.request_delivery_date or False,
            'billing_document': search_product.product_id.billing_document or "",
            'bill_date': search_product.product_id.bill_date or False,
            'vehicle_wholesale_price': search_product.product_id.vehicle_wholesale_price or False,
            'broker_declaration_date': search_product.product_id.broker_declaration_date or False,
            'declaration_date': search_product.product_id.declaration_date or False,
            'netval': search_product.product_id.netval or False,
            'vat_amount': search_product.product_id.vat_amount or False,
        })
        return search_product
