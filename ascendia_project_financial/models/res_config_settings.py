# -*- coding: utf-8 -*-

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'project.config.settings'

    price = fields.Float(
        related='company_id.price',
        string="Default Price E/H",
        readonly=False
    )
