# -*- coding: utf-8 -*-
from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    task_ids = fields.One2many(
        'project.task',
        'assigned_partner_id',
        string='Tasks')
    project_count = fields.Integer(
        '# Projects',
        compute='_compute_project_count')

    @api.multi
    def _compute_project_count(self):
        proj = self.env['project.project']
        for part in self:
            part.project_count = len(proj.search([('partner_id', '=',
                                                   part.id)]))

    @api.multi
    def action_schedule_project(self):
        self.ensure_one()
        action = self.env.ref('project.open_view_project_all_config').read()[0]
        action['context'] = {
            'search_default_partner_id': self.id,
            'default_partner_id': self.id,
            'default_name': self.name,
        }
        return action
