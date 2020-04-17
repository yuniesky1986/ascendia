# -*- coding: utf-8 -*-

from odoo import models, api, fields
from datetime import date


class CRMLead(models.Model):
    _inherit = 'crm.lead'

    name = fields.Char(
        string="Opportunity",
        compute="get_name")

    @api.one
    def get_name(self):
        name = "OP.%s" % str(self.id)
        if self.stage_id:
            name += ".%s" % self.stage_id.name
        if self.partner_id:
            name += ".%s" % self.partner_id.name
        if self.project_type_id:
            name += ".%s" % self.project_type_id.name
        if self.business_area:
            name += ".%s" % self.business_area
        name += ".%s" % str(date.today().year)
        self.name = name
