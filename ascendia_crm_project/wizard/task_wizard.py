# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from datetime import datetime


class TaskWizard(models.TransientModel):
    _name = "task.wizard"

    name = fields.Char(
        string='Task Title',
        track_visibility='always',
        required=True,
        index=True)
    user_id = fields.Many2one('res.users',
        string='Assigned to',
        default=lambda self: self.env.uid,
        index=True,
        track_visibility='always')
    start_date = fields.Datetime(
        string="Start Date")
    date_deadline = fields.Date(
        string='Deadline',
        index=True,
        copy=False)
    tag_ids = fields.Many2many(
        'project.tags',
        string='Tags')
    description = fields.Html(
        string='Description')
    sequence = fields.Integer(
        string='Sequence',
        index=True,
        default=10,
        help="Gives the sequence order when displaying a list of tasks.")
    partner_id = fields.Many2one('res.partner',
        string='Customer')
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env['res.company']._company_default_get())
    displayed_image_id = fields.Many2one(
        'ir.attachment',
        domain="[('res_model', '=', 'project.task'), ('res_id', '=', id), ('mimetype', 'ilike', 'image')]",
        string='Displayed Image')
    open_lead_id = fields.Many2one(
        'crm.lead',
        'Lead',
        required=True)
    open_task_id = fields.Many2one(
        'project.task',
        'Task')

    @api.model
    def default_get(self, fields):
        res = super(TaskWizard, self).default_get(fields)
        if self.env.context.get('active_id') and \
                self.env.context.get('active_model') == 'crm.lead':
            lead = self.env['crm.lead'].browse(self.env.context.get('active_id'))
            res['user_id'] = lead.user_id.id
            res['start_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            res['date_deadline'] = lead.date_deadline
            res['partner_id'] = lead.partner_id.id
            res['open_lead_id'] = lead.id
            if lead.task_id:
                res['open_task_id'] = lead.task_id.id
                res['name'] = lead.task_id.name
                res['user_id'] = lead.task_id.user_id.id
                res['start_date'] = lead.task_id.start_date
                res['date_deadline'] = lead.task_id.date_deadline
                res['tag_ids'] = [(6, 0, [x.id for x in lead.task_id.tag_ids])]
                res['description'] = lead.task_id.description
                res['sequence'] = lead.task_id.sequence
                res['partner_id'] = lead.task_id.partner_id.id
                res['displayed_image_id'] = lead.task_id.displayed_image_id.id
        return res

    @api.one
    def action_save(self):
        values = {'name': self.name,
                  'user_id': self.user_id.id,
                  'start_date': self.start_date,
                  'date_deadline': self.date_deadline,
                  'tag_ids': [(6, 0, [x.id for x in self.tag_ids])],
                  'description': self.description,
                  'sequence': self.sequence,
                  'partner_id': self.partner_id.id,
                  'displayed_image_id': self.displayed_image_id.id}
        if self.open_task_id:
            self.open_task_id.write(values)
        else:
            values.update({'lead_id': self.open_lead_id.id})
            self.env['project.task'].create(values)
        self.open_lead_id.get_last_task()
        return True
