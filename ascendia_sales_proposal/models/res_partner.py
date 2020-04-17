from odoo import fields, models, api,_
from odoo.exceptions import ValidationError


class Partner(models.Model):
    _inherit = 'res.partner'

    dni = fields.Char("DNI")
   