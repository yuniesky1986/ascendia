from odoo import fields, models, api, _


class ProjectProject(models.Model):
    _inherit = 'project.project'

    lead_id = fields.Many2one(
        'crm.lead',
        string='Opportunity')


class ProjectTask(models.Model):
    _inherit = 'project.task'

    @api.model
    def _default_lead_id(self):
        if 'default_lead_id' in self._context:
            return self._context['default_lead_id']
        if self._context.get('active_model') == 'crm.lead':
            return self._context.get('active_id')
        if self._context.get('active_model') == 'project.project':
            proj = self.env['project.project']
            proj_id = proj.browse(self._context.get('active_id'))
            if proj_id.lead_id:
                return proj_id.lead_id.id
        return False

    lead_id = fields.Many2one(
        'crm.lead',
        string='Opportunity',
        default=_default_lead_id)
    sale_order_id = fields.Many2one(
        'sale.order',
        string='Sale Order')
    purchase_order_id = fields.Many2one(
        'purchase.order',
        string='Purchase Order')
    request_id = fields.Many2one(
        'ascendia.price.request',
        string='Price Request')
    proposal_id = fields.Many2one(
        'ascendia.sale.proposal',
        string='Contract')
    product_id = fields.Many2one(
        'product.template',
        string='Product')
    invoice_id = fields.Many2one(
        'account.invoice',
        string='Invoice')
    assigned_partner_id = fields.Many2one(
        'res.partner',
        string='Partner')
    res_user_ids = fields.Many2many(
        'res.users',
        'task_users_rel',
        'task_id',
        'user_id',
        string="Assigned to")
    date_deadline = fields.Datetime(
        string='Deadline',
        index=True,
        copy=False)
    event_id = fields.Many2one(
        'calendar.event',
        string='Calendar Event')
    training_credits_id = fields.Many2one(
        'ascendia.training.credits',
        string='Training Credits')

    @api.model
    def create(self, vals):
        res = super(ProjectTask, self).create(vals)
        event = self.env['calendar.event']
        partner_ids = [x.partner_id.id for x in res.res_user_ids]
        event_vals = {'name': res.name,
                      'partner_ids': [(6, 0, [partner_ids])],
#                      'start_date': str(res.start_date)[:10],
#                      'stop_date': str(res.date_deadline)[:10],
                      'start_datetime': res.start_date,
                      'start': res.start_date,
                      'stop': res.date_deadline,
                      'allday': False,
                      'description': res.description,
                      'privacy': 'private',
                      'show_as': 'busy',
                      'user_id': res.user_id.id}
        res.event_id = event.sudo().create(event_vals).id
        return res
