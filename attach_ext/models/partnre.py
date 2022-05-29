from odoo import fields, models, api


class ResPartnerInherit(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    gender = fields.Selection([('man', 'Man'), ('woman', 'Woman')])

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

    @api.onchange('company_type')
    def onchange_company_type(self):
        self.id_card_iqama = False
        self.id_card_iqama_filename = False
        self.license_driving = False
        self.license_driving_filename = False
        self.cr = False
        self.cr_filename = False
        self.tax_certificate = False
        self.tax_certificate_filename = False
        self.national_address = False
        self.national_address_filename = False