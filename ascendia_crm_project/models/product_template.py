from odoo import fields, models 


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    task_ids = fields.One2many(
        'project.task',
        'product_id',
        string="Tasks")
