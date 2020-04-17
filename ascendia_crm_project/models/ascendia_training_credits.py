from odoo import fields, models


class TrainingCredits(models.Model):
    _inherit = 'ascendia.training.credits'

    task_ids = fields.One2many(
        'project.task',
        'training_credits_id',
        string="Tasks")
