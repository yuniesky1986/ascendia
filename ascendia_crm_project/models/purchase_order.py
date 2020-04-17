from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    task_ids = fields.One2many(
        'project.task',
        'purchase_order_id',
        string="Tasks")
