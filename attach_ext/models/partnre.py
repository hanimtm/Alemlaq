from odoo import fields, models


class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    # gender = fields.Selection([('man', 'Man'), ('woman', 'Woman')])

    id_card_iqama = fields.Binary(string='ID Card/Iqama')
    id_card_iqama_filename = fields.Char()

    license_driving = fields.Binary(string='License Driving')
    license_driving_filename = fields.Char(tracking=True)

    cr = fields.Binary(string='Commercial Register')
    cr_filename = fields.Char()

    tax_certificate = fields.Binary(string='Tax Certificate')
    tax_certificate_filename = fields.Char()

    national_address = fields.Binary(string='National Address')
    national_address_filename = fields.Char()
