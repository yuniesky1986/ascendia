# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.addons import decimal_precision as dp

class Certificate(models.Model):
    _name = 'certificate'
    _inherit = ['mail.thread']

    title = fields.Char('Title')
    task_ids = fields.Many2many(
        'project.task',
        string="Tasks")

