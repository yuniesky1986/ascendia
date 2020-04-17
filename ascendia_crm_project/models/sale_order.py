from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    project_type_id = fields.Many2one(
        'project.type',
        string='Project Type')
    task_ids = fields.One2many(
        'project.task',
        'sale_order_id',
        string="Tasks")

    @api.onchange('proposal_id')
    def onchange_proposal_id(self):
        project_id = False
        if self.proposal_id and self.proposal_id.project_id:
            project_id = self.proposal_id.project_id.id
        self.project_id = project_id
