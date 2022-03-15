from odoo import fields, models, api, tools
from num2words import num2words

# pip install num2words


class AMCLPaymentInherit(models.Model):
    _inherit = 'account.payment'

    # @api.multi
    # def amount_to_text(self, amount, force_lang=False):
    #     self.ensure_one()
    #
    #     def _num2words(number, lang):
    #         try:
    #             return num2words(number, lang=lang).title()
    #         except NotImplementedError:
    #             return num2words(number, lang='en').title()
    #
    #     if num2words is None:
    #         # logging.getLogger(__name__).warning("The library 'num2words' is missing, cannot render textual amounts.")
    #         return ""
    #
    #     formatted = "%.{0}f".format(self.decimal_places) % amount
    #     parts = formatted.partition('.')
    #     integer_value = int(parts[0])
    #     fractional_value = int(parts[2] or 0)
    #
    #     if force_lang:
    #         lang_code = force_lang
    #     else:
    #         lang_code = self.env.user.lang or self.env.context.get('lang')
    #     lang = self.env['res.lang'].search([('code', '=', lang_code)])
    #
    #     amount_words = tools.ustr('{amt_value} {amt_word}').format(
    #         amt_value=_num2words(integer_value, lang=lang.iso_code),
    #         amt_word=self.currency_unit_label,
    #     )
    #     if not self.is_zero(amount - integer_value):
    #         amount_words += ' ' + _('and') + tools.ustr(' {amt_value} {amt_word}').format(
    #             amt_value=_num2words(fractional_value, lang=lang.iso_code),
    #             amt_word=self.currency_subunit_label,
    #         )
    #     return amount_words

    amount_in_word = fields.Char(compute='compute_amount_to_letter')

    @api.depends('amount')
    def compute_amount_to_letter(self):
        for payment in self:
            payment.amount_in_word = num2words(payment.amount, lang='ar_001')

    amount_str_before_point = fields.Char(compute='compute_amount_string')
    amount_str_after_point = fields.Char(compute='compute_amount_string')

    @api.depends('amount')
    def compute_amount_string(self):
        for payment in self:
            payment.amount_str_before_point = str(payment.amount).split('.')[0]
            payment.amount_str_after_point = str(payment.amount).split('.')[1]


