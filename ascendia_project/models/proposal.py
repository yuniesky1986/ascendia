from odoo import models, api, fields, _


class SaleProposal(models.Model):
    _inherit = 'ascendia.sale.proposal'

    project_id = fields.Many2one(
        'project.project',
        string="Project")

    @api.one
    def action_create_project(self):
        if self.state == 'approved':
            proj = self.env['project.project']
            vals = {'name': _("Project: %s" % self.partner_id.name),
                    'partner_id': self.partner_id.id,
                    'contact_id': self.partner_id.child_ids and \
                        self.partner_id.child_ids[0].id or False,
                    'proposal_id': self.id,
                    'start_date': self.approval_date,
                    'end_date': self.request_date}
            self.project_id = proj.create(vals)
