from odoo import models, fields, api
from datetime import date


class Stage(models.Model):
    _inherit = 'crm.stage'

    can_be_create = fields.Boolean(
        string="Can be create Price Request")
