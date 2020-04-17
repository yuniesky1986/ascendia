from odoo import fields, models


class Department(models.Model):

    _name = 'ascendia.department'

    name = fields.Char("Name")
