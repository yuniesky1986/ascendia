# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.addons import decimal_precision as dp

class Student(models.Model):
    _name = 'student'
    _inherit = ['mail.thread']

    name = fields.Char(string='Name', required=True)
    first_last_name = fields.Char(string='First last name')
    second_last_name = fields.Char(string='Second last name')
    date_birth = fields.Date('Date birth')
    dni = fields.Char(string='Dni')
    sex = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ],string='Sex', copy=False, index=True)
#    city_id = fields.Many2one(
#        'city',
#        string="City")
    city = fields.Char('City')
    state_id = fields.Many2one(
        'res.country.state',
        string='State')
    zip = fields.Char(string='Zip')
    email = fields.Char(string="Email")
    mobile = fields.Char(string="Mobile")
    phone = fields.Char(string="Phone")
    fax = fields.Char(string="Fax")
    course_ids = fields.Many2many(
        'course',
        string="Courses")
    responsible = fields.Selection([
        ('ascendia', 'Ascendia'),
        ('anfora', 'Anfora'),
        ],string='Responsible', copy=False, index=True)
    is_request = fields.Boolean(string='Is request')
    missing_doc = fields.Boolean(string='Missing doc')
    doc_type = fields.Char(string="Doc type")
    in_gefoc = fields.Boolean(string='In GEFOC')
    is_student = fields.Boolean(string='Is student', default=False)
    pre_selection = fields.Selection([
        ('admited', 'Admited'),
        ('excluded', 'Excluded'),
        ],string='Pre-selection', copy=False, index=True)
    initial_selection = fields.Selection([
        ('admited', 'Admited'),
        ('reserve', 'Reserve'),
        ('excluded', 'Excluded'),
        ],string='Initial Selection', copy=False, index=True)
    reserve_number = fields.Integer(string="Reserve number")
    state_change = fields.Selection([
        ('admited', 'Admited'),
        ('renounce', 'Renounce'),
        ],string='State change', copy=False, index=True)
    renounce = fields.Selection([
        ('laboral_insertion', 'Laboral Insertion'),
        ('other_selection_center', 'Other Selection Center'),
        ('personal_motives', 'Personal Motives'),
        ],string='Renounce', copy=False, index=True)
    date_renounce = fields.Date('Date renounce')
    formative_action = fields.Text('Formative action')
    task_ids = fields.Many2many(
        'project.task',
        string="Tasks")

    @api.model
    def create(self, values):
        if self._context.get('student', False):
            values.update({'is_student': True})
        return super(Student, self).create(values)

    @api.multi
    def to_student(self):
        self.write({'is_student': True})
        return {
               'name': _('Student'),
               'view_mode': 'form',
               'res_model': 'student',
               'res_id': self.id,
               'view_id' : self.env.ref('ascendia_podio.student_form_view').id,
               'type': 'ir.actions.act_window',
               'domain': [('id', '=', self.id)],
               'context': {'form_view_initial_mode': 'edit','force_detailed_view': True},
               }




