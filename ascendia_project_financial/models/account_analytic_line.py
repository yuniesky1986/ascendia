# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import fields, models, api, _


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    employee_id = fields.Many2one(
        comodel_name='hr.employee',
        string="Employee"
    )
    price = fields.Monetary(
        string="Price E/H",
    )

    @api.onchange('employee_id')
    def onchange_employee_id(self):
        user_id = False
        if self.employee_id:
            self.price = self.employee_id.timesheet_cost
            user_id = self.employee_id.user_id.id
        if not user_id:
            user_id = self.env.context.get('user_id', self.env.user.id)
        self.user_id = user_id

    @api.onchange('price', 'unit_amount')
    def _onchange_cal_amount(self):
        if self.price and self.unit_amount:
            amount = self.price * self.unit_amount
            amount_converted = amount
            if amount_converted > 0:
                amount_converted = amount_converted * -1
            self.amount = amount_converted
