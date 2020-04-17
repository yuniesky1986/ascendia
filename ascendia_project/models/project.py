from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from datetime import datetime

BUSINESS_AREA_LIST = [('ssi', 'SSI'),
                      ('sgc', 'SGC'),
                      ('ssf', 'SSF'),
                      ('asc', 'ASC'),
                      ('cav', 'CAV'),
                      ('sgidi', 'SGIDI'),
                      ('sge', 'SGE')]

class ProjectType(models.Model):
    _name = 'project.type'

    name = fields.Char(
        string="Name")

# class ClasificationTask(models.Model):
#     _name = 'clasification.task'
#
#     name = fields.Char(
#         string="Name")
#     ponderation = fields.Float(
#         string="Ponderation")


class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    code = fields.Selection(
        [('draft', 'Draft'),
         ('pending', 'Pending start'),
         ('dev', 'In development'),
         ('paused', 'Paused'),
         ('closed', 'Closed'),
         ('canceled', 'Canceled')],
        string='Code',
        default='draft')


class ProjectTask(models.Model):
    _inherit = 'project.task'

    start_date = fields.Datetime(
        string="Start Date")
    user_ids = fields.Many2many(
        'res.users',
        string="Technical",
        related='project_id.user_ids')
    user_id = fields.Many2one('res.users',
        string='Assigned to',
        index=True,
        default=False,
        track_visibility='always')
    # clasification = fields.Many2one('clasification.task',
    #     string='Clasification task',
    #     index=True,
    #     default=False,
    #     track_visibility='always')
    ponderation = fields.Float(
        string='Ponderation',
        related='clasification_id.ponderation',
        readonly='True')
    clasification_id = fields.Many2one(
        'clasification.task',
        string='Clasification')

    @api.depends('stage_id', 'timesheet_ids.unit_amount', 'planned_hours', 'child_ids.stage_id',
                 'child_ids.planned_hours', 'child_ids.effective_hours', 'child_ids.children_hours', 'child_ids.timesheet_ids.unit_amount')
    def _hours_get(self):
        for task in self.sorted(key='id', reverse=True):
            children_hours = 0
            for child_task in task.child_ids:
                if child_task.stage_id and child_task.stage_id.fold:
                    children_hours += child_task.effective_hours + child_task.children_hours
                else:
                    children_hours += max(child_task.planned_hours, child_task.effective_hours + child_task.children_hours)

            task.children_hours = children_hours
            task.effective_hours = sum(task.timesheet_ids.mapped('unit_amount'))
            task.remaining_hours = task.planned_hours - task.effective_hours - task.children_hours
            task.total_hours = max(task.planned_hours, task.effective_hours)
            task.total_hours_spent = task.effective_hours + task.children_hours
            task.delay_hours = max(-task.remaining_hours, 0.0)

            if task.stage_id and task.stage_id.code == 'closed':
                task.progress = 100.0
            elif (task.planned_hours > 0.0):
                task.progress = round(100.0 * (task.effective_hours + task.children_hours) / task.planned_hours, 2)
            else:
                task.progress = 0.0

    @api.one
    def get_compute_url(self):
        server = self.env['ir.config_parameter'].get_param('web.base.url')
        menu = self.env['ir.model.data'].xmlid_to_res_id(
            'project.menu_action_view_task')
        action = self.env['ir.model.data'].xmlid_to_res_id(
            'project.action_view_task')
        url = "%s/web#id=%s&view_type=form" \
              "&model=project.task" \
              "&menu_id=%s&action=%s" \
              % (server, self.id, menu, action)
        return url

    @api.one
    def send_email(self):
        tpl = 'ascendia_project.email_template_new_task'
        template = self.env.ref(tpl, False)
        if template:
            template.sudo().send_mail(self.id)

    @api.model
    def create(self, vals):
        ponderation = 0
        if vals.get('project_id'):
            project = self.env['project.project'].search([('id','=',vals.get('project_id'))])
            for task in project.task_ids:
                ponderation += task.ponderation
        if vals.get('clasification_id'):
            clasif = self.env['clasification.task'].search([('id','=',vals.get('clasification_id'))])
            ponderation += clasif.ponderation
        if ponderation > 100:
            raise ValidationError(_('The total of ponderation task for this project excede 100%, readjust tasks.'))
        res = super(ProjectTask, self).create(vals)
        # res.send_email()
        return res


class ProjectIssue(models.Model):
    _inherit = 'project.issue'

    user_ids = fields.Many2many(
        'res.users',
        string="Technical",
        related='project_id.user_ids')

    @api.onchange('project_id')
    def onchange_project_id(self):
        if self.project_id:
            self.partner_id = self.project_id.partner_id


class ProjectStates(models.Model):
    _name = 'project.states'

    name = fields.Char(
        string="Name")


class ClasificationTask(models.Model):
    _name = 'clasification.task'

    name = fields.Char(
        string="Name")
    ponderation = fields.Float(
        string="Ponderation")


class Project(models.Model):
    _inherit = 'project.project'

    @api.one
    @api.depends('end_date', 'start_date')
    def _get_days(self):
        days = 0
        if self.end_date and self.start_date:
            close_date = fields.Date.from_string(self.end_date)
            start_date = fields.Date.from_string(self.start_date)
            days = (close_date - start_date).days
        self.days = days

    teoric_hours = fields.Float(
        string='Teoric hours'
    )

    @api.one
    def _get_real_hours(self):
        analytic_line = self.env['account.analytic.line']
        line_ids = analytic_line.search([('project_id', '=', self.id)])
        self.real_hours = sum(line_ids.mapped('unit_amount'))

    real_hours = fields.Float(
        string='Real hours',
        compute='_get_real_hours'
    )

    @api.one
    @api.depends('teoric_hours')
    def _get_pending_hours(self):
        self.ensure_one()
        self.pending_hours = self.teoric_hours - self.real_hours

    pending_hours = fields.Float(
        string='Pending hours',
        compute='_get_pending_hours',
    )

    @api.one
    @api.depends('teoric_hours')
    def _get_progess_time(self):
        self.ensure_one()
        if self.teoric_hours and self.real_hours:
           self.progress_time = self.real_hours * 100 / self.teoric_hours

    progress_time = fields.Float(
        string='Progress Time',
        compute='_get_progess_time',
    )

    @api.one
    def _get_progress_task(self):
        progress = 0
        task = self.env['project.task']
        task_type = self.env['project.task.type']
        stage_ids = task_type.search([('code', '=', 'canceled')])
        if stage_ids:
            task_ids = task.search([('stage_id', 'not in',
                                     [x.id for x in stage_ids])])
        else:
            task_ids = task.search([])
        total = len(task_ids)
        closed_ids = task_type.search([('code', '=', 'closed')])
        if closed_ids and total:
            task_closed_ids = task.search([('stage_id', 'in',
                                            [x.id for x in closed_ids])])
            closed = len(task_closed_ids)
            progress = closed * 100 / total
        self.progress = progress

    progress_task = fields.Float(
        string="Progress",
        compute='_get_progress_task',
        store='True'
    )
    project_type_id = fields.Many2one(
        'project.type',
        string='Type'
    )
    contact_id = fields.Many2one(
        'res.partner',
        string='Contact'
    )
    proposal_id = fields.Many2one(
        'ascendia.sale.proposal',
        'Contract'
    )
    start_date = fields.Date(
        string="Start date"
    )
    next_date = fields.Datetime(
        string="Next Date"
    )
    end_date = fields.Date(
        string="End date"
    )
    close_date = fields.Datetime(
        string="Close Date"
    )
    proposal_due_date = fields.Date(
        string="Due Date",
        related='proposal_id.request_date'
    )
    charge_id = fields.Many2one(
        'crm.charge',
        string="Charge"
    )
    user_ids = fields.Many2many(
        'res.users',
        string="Technical"
    )
    state_ids = fields.Many2many(
        'project.states',
        string="Project States"
    )
    state = fields.Selection(
        [('draft', 'Draft'),
         ('pending', 'Pending start'),
         ('dev', 'In development'),
         ('paused', 'Paused'),
         ('closed', 'Closed'),
         ('canceled', 'Canceled')],
        string='State',
        readonly=True,
        default='draft'
    )
    days = fields.Integer(
        string="Days",
        compute='_get_days'
    )
    observations = fields.Text(
        'Observations'
    )
    business_area = fields.Selection(
        BUSINESS_AREA_LIST,
        'Business Area'
    )
    teoric_visits = fields.Integer(
        string='Teoric visits'
    )
    real_visits = fields.Integer(
        string='Real visits'
    )
    task_ids = fields.One2many(
        'project.task',
        'project_id',
        string='Task',
        domain=[]
    )

    @api.onchange('partner_id', 'start_date', 'end_date')
    def onchange_partner_id(self):
        if self.partner_id:
            self.contact_id = self.partner_id.child_ids and \
                self.partner_id.child_ids[0] or False
            if self.start_date and self.end_date:
                proposal = self.env['ascendia.sale.proposal']
                proposal_id = proposal.search([('partner_id', '=',
                                                self.partner_id.id),
                                               ('private_state', '=',
                                                'approved'),
                                               ('approval_date', '<=',
                                                self.start_date),
                                               ('request_date', '>=',
                                                self.end_date)],
                                              limit=1)
                self.proposal_id = proposal_id or False

    @api.one
    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        if self.start_date and self.end_date:
            if self.end_date < self.start_date:
                raise ValidationError(_('The End Date cannot be less than '
                                        'Start Date.'))
            elif self.proposal_id and \
                    self.proposal_id.approval_date and \
                    self.proposal_id.request_date:
                flag = False
                if self.start_date < self.proposal_id.approval_date or \
                        self.start_date > self.proposal_id.request_date:
                    flag = True
                elif self.start_date > self.proposal_id.request_date:
                    flag = True
                if flag:
                    raise ValidationError(_('The start and end dates of '
                                            'the project must be between '
                                            'the approval and expiration '
                                            'dates of the contract.'))
