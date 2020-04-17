from odoo import fields, models, api
from datetime import date


class CRMLead(models.Model):
    _inherit = 'crm.lead'

    project_type_id = fields.Many2one(
        'project.type',
        string='Product')
    task_ids = fields.One2many(
        'project.task',
        'lead_id',
        string="Tasks")
    task_date = fields.Char(
        string="Last Task Date",
        compute='get_last_task')
    task_title = fields.Char(
        string="Lask Task Title",
        compute='get_last_task')
    task_id = fields.Many2one(
        'project.task',
        string="Last Task",
        compute='get_last_task')

    kanban_state = fields.Selection(
        [('grey', 'No task add'),
         ('red', 'Task date late'),
         ('green', 'Task is planned')],
        string='Task State',
        compute='_compute_kanban_state')
    project_count = fields.Integer(
        '# Projects',
        compute='_compute_project_count')

    @api.multi
    def _compute_kanban_state(self):
        today = date.today()
        for lead in self:
            kanban_state = 'grey'
            if lead.task_date:
                lead_date = fields.Date.from_string(lead.task_date)
                if lead_date >= today:
                    kanban_state = 'green'
                else:
                    kanban_state = 'red'
            lead.kanban_state = kanban_state

    @api.multi
    def _compute_project_count(self):
        proj = self.env['project.project']
        for lead in self:
            lead.project_count = len(proj.search([('lead_id', '=', lead.id)]))

    @api.one
    def get_last_task(self):
        task_date = ''
        task_title = ''
        task_id = False
        if self.task_ids:
            task_date = self.task_ids[0].start_date and self.task_ids[0].start_date[0:10]
            task_title = self.task_ids[0].name
            task_id = self.task_ids[0].id
        self.task_date = task_date
        self.task_title = task_title
        self.task_id = task_id

    @api.one
    def action_create_price_request(self):
        res = super(CRMLead, self).action_create_price_request()
        if self.request_id and self.project_type_id:
            self.request_id.project_type_id = self.project_type_id.id
        return res

    @api.multi
    def action_schedule_project(self):
        self.ensure_one()
        action = self.env.ref('project.open_view_project_all_config').read()[0]
        action['context'] = {
            'search_default_lead_id': self.id,
            'default_lead_id': self.id,
            'default_partner_id': self.partner_id.id,
            'default_name': self.name,
            'default_lead_id': self.id,
            'default_start_date': self.start_date,
            'default_end_date': self.date_deadline,
            'default_user_ids': [(6, 0, [x.id for x in self.technical_ids])],
        }
        return action


class PriceRequest(models.Model):
    _inherit = 'ascendia.price.request'

    project_type_id = fields.Many2one(
        'project.type',
        string='Project Type')

    @api.one
    def action_create_sale_order(self):
        res = super(PriceRequest, self).action_create_sale_order()
        if self.project_type_id:
            for sale in self.sale_order_ids:
                sale.project_type_id = self.project_type_id.id
        return res
