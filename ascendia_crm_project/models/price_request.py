from odoo import fields, models


class PriceRequest(models.Model):
    _inherit = 'ascendia.price.request'

    task_ids = fields.One2many(
        'project.task',
        'request_id',
        string="Tasks")
