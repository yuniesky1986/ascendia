# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class City(models.Model):
    _name = 'city'

    state_id = fields.Many2one(
        'res.country.state',
        string='State')
    name = fields.Char(
        string='Name',
        required=True)
    code = fields.Char(
        string='Code',
        help='The city code.')
