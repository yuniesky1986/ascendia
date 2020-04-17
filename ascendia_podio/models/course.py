# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.addons import decimal_precision as dp

class Course(models.Model):
    _name = 'course'
    _inherit = ['mail.thread']

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code')
    total_hours = fields.Char(string='Total hours')
    teoric_hours = fields.Char(string='Teoric hours')
    practic_hours = fields.Char(string='Practic hours')
    number = fields.Integer(string="Number")
    price = fields.Float('Price')
    quotation = fields.Float('Quotation')
    member_id = fields.Many2one(
        'res.users',
        string="Member")
    url_link = fields.Text('Url link')
    task_ids = fields.Many2many(
        'project.task',
        string="Tasks")

