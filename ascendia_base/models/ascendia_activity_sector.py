from odoo import fields, models, api


class ActivitySector(models.Model):
    _name = 'ascendia.activity.sector'
    _rec_name = 'display_name1'

    name = fields.Char(
        string="Name",
        required=True)

    @api.onchange('name', 'parent_id')
    def onchange_get_display_name(self):
        name = ''
        if self.parent_id:
            name += self.parent_id.name
            name += '>'
        if self.name:
            name += self.name
        self.display_name1 = name

    display_name1 = fields.Char(
        string="Diplay Name")
    parent_id = fields.Many2one(
        'ascendia.activity.sector',
        string="Primary sector")
