# -*- coding: utf-8 -*-

import binascii
from num2words import num2words
from odoo import api, models, fields,_
from datetime import datetime
import pytz
import base64

class AccountMove(models.Model):
    _inherit = "account.move"

    TAG_SELLER = 1
    TAG_VAT_NO = 2
    TAG_TIME_STAMP = 3
    TAG_TOTAL = 4
    TAG_VAT_TOTAL = 5

    arebic_date = fields.Char("Arabic Date")
    invoice_date_time = fields.Datetime('Invoice Date Time')

    def _data_hex(self, value, tag):
        hex_tag = self._convert_int_to_hex(tag)
        hex_len = self._convert_int_to_hex(len(value.encode("UTF-8")))
        hex_val = self._convert_str_to_hex(value)
        return "%s%s%s" % (hex_tag, hex_len, hex_val)

    def _seller_hex(self, value):
        return self._data_hex(value, self.TAG_SELLER)

    def _vat_no_hex(self, value):
        return self._data_hex(value, self.TAG_VAT_NO)

    def _time_stamp_hex(self, value):
        return self._data_hex(value, self.TAG_TIME_STAMP)

    def _total_hex(self, value):
        return self._data_hex(value, self.TAG_TOTAL)

    def _vat_total_hex(self, value):
        return self._data_hex(value, self.TAG_VAT_TOTAL)

    def _convert_int_to_hex(self, value):
        return "%0.2x" % value

    def _convert_str_to_hex(self, value):
        hex_val = ""
        if value:
            str_bytes = value.encode("UTF-8")
            encoded_hex = binascii.hexlify(str_bytes)
            hex_val = encoded_hex.decode("UTF-8")

        return hex_val

    def _convert_text_to_base64(self, value):
        # value_bytes = value.decode('utf-8')
        base64_bytes = base64.b64encode(value)
        return base64_bytes.decode("utf-8")

    def generate_tlv_code(self):
        self.invalidate_cache()
        DEFAULTE_TZ = 'Asia/Riyadh'
        hex_seller = False
        hex_vat_no = False
        hex_time_stamp = False
        total = False
        vat_total = False
        # time_stamp = datetime.now(
        #     pytz.timezone(self.env.user.tz or self._context.get('tz', DEFAULTE_TZ))).strftime('%Y-%m-%dT%H:%M:%SZ')

        localFormat = "%Y-%m-%d %H:%M:%S"

        # Convert date to current user timezone or Saudi Arabia in default case.
        if self.invoice_date_time:
            utcmoment_naive = datetime.strptime(str(self.invoice_date_time), localFormat)
        else:
            utcmoment_naive = self.create_date
        utcmoment = utcmoment_naive.replace(tzinfo=pytz.utc)

        tz_ = self.env.user.tz or self._context.get('tz', DEFAULTE_TZ)
        localDatetime = utcmoment.astimezone(pytz.timezone(tz_))

        time_stamp = localDatetime.strftime('%Y-%m-%dT%H:%M:%SZ')
        hex_seller = self._seller_hex(self.company_id.name or "")
        hex_vat_no = self._vat_no_hex(self.company_id.vat or "")
        hex_time_stamp = self._time_stamp_hex(time_stamp)
        hex_total = self._total_hex(str(self.amount_total))
        hex_vat_total = self._vat_total_hex(str(self.amount_tax))

        hex_text = "%s%s%s%s%s" % (hex_seller, hex_vat_no, hex_time_stamp, hex_total, hex_vat_total)
        code_qr = self._convert_text_to_base64(bytearray.fromhex(hex_text))

        return code_qr