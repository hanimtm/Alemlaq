from odoo import fields, models


class IrTranslate(models.Model):
    _inherit = 'ir.translation'

    def write(self, vals):
        """
        update Value for Other
        :param vals:
        :return:
        """
        if not self._context.get('no_update_next') and vals and 'value' in vals:
            for rec in self:
                same_translation = self.search([
                    ('id', '!=', rec.id), ('src', '=', rec.src), ('lang', '=', 'ar_001'),
                    ('name', 'in', ['product.template,name', 'product.template,exterior_color_code',
                                    'product.template,exterior_color', 'product.template,interior_color_code',
                                    'product.template,interior_color', 'product.template,brand',
                                    'product.template,vehicle_model', 'product.template,model_code',
                                    'product.template,description'])])
                print ('-- Update Record -->', same_translation)
                if same_translation:
                    same_translation.with_context({'no_update_next': True}).write({'value': vals.get('value')})
        res = super(IrTranslate, self).write(vals)
        return res
