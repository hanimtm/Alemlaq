# -*- coding: utf-8 -*-
# Part of AHCEC/VEICO.

import base64
import csv
from datetime import datetime
import datetime
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
                    Updated_record_list = []

                    for row in range(sheet.nrows):
                        try:
                            if skip_header:
                                skip_header = False
                                counter = counter + 1
                                continue
                            print('Picking :: ', picking)
                            if picking.move_lines:

                                move = picking.move_lines.sudo().filtered(
                                    lambda p: p.product_id.default_code == sheet.cell(row, 2).value)
                                print('Picking :: ', move)
                                if not move:
                                    not_found_records.append(sheet.cell(row, 2).value)
                                    continue

                                if not_found_records:
                                    raise UserError(_('Not Found the Record %s.', not_found_records))

                                if move:
                                    type = False
                                    if sheet.cell(row, 4).value == 'AUTOMATIC':
                                        type = 'automatic'
                                    elif sheet.cell(row, 4).value == 'CVT':
                                        type = 'cvt'
                                    else:
                                        type = 'manual'

                                    move.sudo().write({'complete_engine_number': sheet.cell(row, 3).value or "",
                                                'transmission_type':type,
                                                'billing_document': str(sheet.cell(row, 5).value).split('.')[0] or "",
                                                'bill_date': datetime.datetime.strptime(str(int(sheet.cell(row, 6).value)), '%Y%m%d').date() or False,
                                                'key_number': str(sheet.cell(row, 7).value).split('.')[0] or "",
                                                'vessel_no': str(sheet.cell(row, 8).value).split('.')[0] or "",
                                                'card_no': str(sheet.cell(row, 9).value).split('.')[0] or "",
                                                })
                                    move.product_id.product_tmpl_id.sudo().write({
                                        'product_vc': sheet.cell(row, 0).value or "",
                                        'key_number': move.key_number,
                                        'vessel_no': move.vessel_no,
                                        'card_no': move.card_no,
                                    })
                                    if move.purchase_line_id:
                                        move.purchase_line_id.sudo().write({
                                            'complete_engine_number': move.complete_engine_number,
                                            'transmission_type': move.transmission_type,
                                            'billing_document': move.billing_document,
                                            'bill_date': move.bill_date,
                                            'key_number': move.key_number,
                                            'vessel_no': move.vessel_no,
                                            'card_no': move.card_no,
                                        })

                                    if move.sale_line_id:
                                        move.sale_line_id.sudo().write({
                                            'complete_engine_number': move.complete_engine_number,
                                            'transmission_type': move.transmission_type,
                                            'billing_document': move.billing_document,
                                            'bill_date' : move.bill_date
                                        })

                                    Updated_record_list.append(move.id)
                                    counter = counter + 1
                            else:
                                skipped_line_no[str(counter)] = " - Move not Updated. "
                                counter = counter + 1
                                continue

                        except Exception as e:
                            skipped_line_no[str(counter)] = " - Value is not valid " + ustr(e)
                            counter = counter + 1
                            continue

                except Exception as e:
                    raise UserError(_("Sorry, Your excel file does not match with our format " + ustr(e)))

                if counter > 1:
                    completed_records = len(Updated_record_list)
                    res = self.show_success_msg(completed_records, skipped_line_no)
                    picking.write({'product_imported': True})
                    return res
