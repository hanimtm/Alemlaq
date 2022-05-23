from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    customer_gender = fields.Selection([('man', 'Man'), ('woman', 'Woman')],
                                       string='Gender', default='man')

    id_card_iqama = fields.Binary(tracking=True, string='ID Card/Iqama')
    id_card_iqama_filename = fields.Char(tracking=True)

    license_driving = fields.Binary(tracking=True, string='License Driving')
    license_driving_filename = fields.Char(tracking=True)

    cr = fields.Binary(tracking=True, string='Commercial Register')
    cr_filename = fields.Char(tracking=True)

    tax_certificate = fields.Binary(tracking=True, string='Tax Certificate')
    tax_certificate_filename = fields.Char(tracking=True, )

    national_address = fields.Binary(tracking=True, string='National Address')
    national_address_filename = fields.Char(tracking=True)
