# -*- coding: utf-8 -*-
from odoo import fields, models, api, _


class TrainingCreditsType(models.Model):
    _name = 'ascendia.training.credits.type'

    name = fields.Char(
        string="Name")


class TrainingCreditsYear(models.Model):
    _name = 'ascendia.training.credits.year'

    name = fields.Char(
        string="Name")


class TrainingCreditsMonth(models.Model):
    _name = 'ascendia.training.credits.month'

    name = fields.Char(
        string="Name")
    
class TrainingCreditsWeekDay(models.Model):
    _name = 'ascendia.training.credits.weekday'

    name = fields.Char(
        string="Name")


class TrainingCredits(models.Model):
    _name = 'ascendia.training.credits'
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    name = fields.Char(
        string="Name")
    partner_id = fields.Many2one(
        'res.partner',
        string="Partner")
    lead_id = fields.Many2one(
        'crm.lead',
        string="Pipeline")
    year = fields.Many2one(
        'ascendia.training.credits.year',
        string="Year")
    month = fields.Many2one(
        'ascendia.training.credits.month',
        string="Month")
    drive_url = fields.Char(
        string="Drive link")
    type = fields.Many2many(
        'ascendia.training.credits.type',
        string="Training Credits Type")
    tutor = fields.Many2many(
        comodel_name='res.users',
        relation='res_users_tutor_rel',
        column1='training_tutor_id',
        column2='user_id',
        string='Tutor')
    user_id = fields.Many2many(
        comodel_name='res.users',
        relation='res_users_user_rel',
        column1='training_user_id',
        column2='user_id',
        string="User")
    modality = fields.Selection(
        [('on_site', 'On-site'),
         ('remote', 'Remote'),
         ('on_line', 'On-line'),
         ('abandoned', 'Abandoned')],
        string="Modality")
    accession_agreement = fields.Selection(
        [('yes', 'Yes'),
         ('no', 'No')],
        string="Accession Agreement")
    registration_form = fields.Selection(
        [('yes', 'Yes'),
         ('no', 'No')],
        string="Registration Form")
    certificate = fields.Selection(
        [('yes', 'Yes'),
         ('no', 'No')],
        string="Certificate")
    invoiced = fields.Selection(
        [('yes', 'Yes'),
         ('no', 'No')],
        string="Invoiced")
    documentation_initial_sent = fields.Selection(
        [('yes', 'Yes'),
         ('no', 'No')],
        string="Sent the initial documentation of the course?")
    documentation_end_sent = fields.Selection(
        [('yes', 'Yes'),
         ('no', 'No')],
        string="Sent the ended documentation of the course?")
    documentation_signed = fields.Selection(
        [('yes', 'Yes'),
         ('no', 'No')],
        string="Received the signed document")
    participants = fields.Integer(
        string="Number of Participants")
    amount = fields.Float(
        string="Amount to be bonded")
    wage_cost = fields.Float(
        string="Wage Cost")
    tutoring_schedule = fields.Text(
        string="Tutoring schedule")
    date_start = fields.Datetime(
        string="Start Date")
    date_end = fields.Datetime(
        string="End Date")
    concept = fields.Text(
        string="Concepts")
    text = fields.Text(
        string="Observations")
    morning_schedule = fields.Char('Morning Schedule')
    afternoon_schedule = fields.Char('Afternoon Schedule')
    hour_qty = fields.Integer('Total Hours')
    pres_hour_qty = fields.Integer('Training Hours')
    teacher_id = fields.Many2one('res.users', 'Teacher')
    center_id = fields.Many2one('res.partner', 'Formation Center')
    weekday_ids = fields.Many2many(
        comodel_name='ascendia.training.credits.weekday',
        relation='ascendia_training_weekday_rel',
        column1='training_id',
        column2='weekday_id',
        string="Weekday")
    group_action = fields.Char('Formative Action')
    group_code = fields.Char('Code')
    group_name = fields.Char('Denomination')
    group_description = fields.Char('Description')
    formation_mean = fields.Selection([('external', 'With External Mean'),
                                       ('accredit', 'With Accredit Mean')], 'Formation Mean')
    
