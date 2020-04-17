# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError

class EditionNumber(models.Model):
    _name = 'ascendia.edition.number'
    _description = 'Edition Number'
    
    name = fields.Char('Name')
    

class EditionYear(models.Model):
    _name = 'ascendia.edition.year'
    _description = 'Edition Year'
    _rec_name = 'edition_id' 
    
    edition_id = fields.Many2one('ascendia.edition.number', 'No. Edition Date')
    date = fields.Date('Date')
    certificate_id = fields.Many2one('ascendia.certificate.lopd', 'Certificate', required=True, ondelete="cascade")
    
class Certificate(models.Model):
    _name = 'ascendia.certificate'
    _inherit = ['mail.thread']
    _description = 'Certificate' 
    _rec_name = "partner_id"

    name = fields.Char(string='Name')
    partner_id = fields.Many2one('res.partner', "Organization")
    lead_id = fields.Many2one('crm.lead', "Pipeline")
    task_ids = fields.Many2many(
        'project.task',
        string="Tasks")
    
class FormationCertificate(models.Model):
    _name = 'ascendia.certificate.formation'
    _description = 'Formation Certificate' 
    _inherits = {'ascendia.certificate': 'certificate_id' }
    _inherit = ['mail.thread']
    _rec_name = "partner_id"

    certificate_id = fields.Many2one('ascendia.certificate', "Certificate", required=True, ondelete="cascade")
    year =  fields.Char('Year')
    user_to = fields.Char('User to')
    
class LOPDCertificate(models.Model):
    _name = 'ascendia.certificate.lopd'
    _description = 'LOPD Certificate' 
    _inherits = {'ascendia.certificate': 'certificate_id' }
    _inherit = ['mail.thread']
    _rec_name = "partner_id"

    certificate_id = fields.Many2one('ascendia.certificate', "Certificate", required=True, ondelete="cascade")
    edition_ids =  fields.One2many('ascendia.edition.year', 'certificate_id', 'Edition Dates')
    year = fields.Char('Edition Year')
    
    
class GoodExecutionCertificate(models.Model):
    _name = 'ascendia.certificate.good.execution'
    _description = 'Good Execution Certificate' 
    _inherits = {'ascendia.certificate': 'certificate_id' }
    _inherit = ['mail.thread']
    _rec_name = "partner_id"

    certificate_id = fields.Many2one('ascendia.certificate', "Certificate", required=True, ondelete="cascade")
    user_id = fields.Many2one('res.users', 'Contact')
    state = fields.Selection([('requested', 'Requested'),
                              ('received', 'Received')], 'State')
    
    
    

