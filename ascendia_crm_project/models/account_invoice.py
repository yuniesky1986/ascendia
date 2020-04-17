from odoo import fields, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    task_ids = fields.One2many(
        'project.task',
        'invoice_id',
        string="Tasks")
