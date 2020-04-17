# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.addons import decimal_precision as dp

class Baremation(models.Model):
    _name = 'baremation'
    _inherit = ['mail.thread']

    text_baremation = fields.Char('Text')
    task_ids = fields.Many2many(
        'project.task',
        string="Tasks")

