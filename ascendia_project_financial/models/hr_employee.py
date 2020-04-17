# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    timesheet_cost = fields.Float(
        string='Timesheet Cost',
        currency_field='currency_id',
        default=lambda self: self.env.user.company_id.price
    )
