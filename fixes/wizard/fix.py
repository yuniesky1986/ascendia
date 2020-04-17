# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010, 2014 Tiny SPRL (<http://tiny.be>).
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
from openerp import models, fields, api


class Fixes(models.TransientModel):
    _name = 'fix'

    action = fields.Char(
        string="Action")

    @api.multi
    def execute_this_action(self):
        print "AAAAAAAAAAAAAAA"
        res = False
        if hasattr(self, self.action):
            res = getattr(self, self.action)()
        return res

    @api.model
    def fix_update_invoice_line_analytic_id(self):
        for line in self.env['account.invoice.line'].search([]):
            sale = self.env['sale.order'].search([('name', '=',
                                                   line.invoice_id.origin)],
                                                 limit=1)
            if sale and sale.project_id:
                analytic_id = sale.project_id.analytic_account_id.id
                line.account_analytic_id = analytic_id

    @api.model
    def fix_update_sale_analytic_id(self):
        for sale in self.env['sale.order'].search([]):
            if sale.proposal_id and sale.proposal_id.project_id:
                self.project_id = sale.proposal_id.project_id.analytic_account_id.id

    @api.model
    def fix_update_move_line_analytic_id(self):
        for line in self.search([]):
            if line.account_id.internal_type == 'receivable':
                sale = self.env['sale.order'].search([('name', '=',
                                                       line.invoice_id.origin)],
                                                     limit=1)
                if sale and sale.project_id:
                    analytic_id = sale.project_id.id
                    line.analytic_account_id = analytic_id
                    line.create_analytic_lines()

    @api.model
    def fix_update_activity_sector(self):
        for activity in self.env['ascendia.activity.sector'].search([]):
            if not activity.display_name1:
                name = ''
                if activity.parent_id:
                    name += activity.parent_id.name
                    name += '>'
                if activity.name:
                    name += activity.name
                activity.display_name1 = name

    @api.model
    def fix_update_lead_partner_id(self):
        for lead in self.env['crm.lead'].search([]):
            if lead.podio_org_id:
                part_id = self.env['res.partner'].search([('podio_id', '=',
                                                           lead.podio_org_id)],
                                                         limit=1)
                lead.partner_id = part_id.id
