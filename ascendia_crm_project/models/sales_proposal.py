# -*- coding: utf-8 -*-
from odoo import fields, models, api


class SaleProposal(models.Model):
    _inherit = 'ascendia.sale.proposal'

    task_ids = fields.One2many(
        'project.task',
        'proposal_id',
        string="Tasks")
    lead_id = fields.Many2one(
        'crm.lead',
        string="Opportunity")

    @api.one
    def action_create_project(self):
        res = super(SaleProposal, self).action_create_project()
        if self.state == 'approved' and self.lead_id:
            self.project_id.project_type_id = self.lead_id.project_type_id.id
        return res

    @api.onchange('lead_id')
    def onchange_lead_id(self):
        self.partner_id = False
        if self.lead_id:
            self.partner_id = self.lead_id.partner_id.id
