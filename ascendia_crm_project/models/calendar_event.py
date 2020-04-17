from odoo import fields, models


class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    description = fields.Html(
        string='Description',
        states={'done': [('readonly', True)]})
