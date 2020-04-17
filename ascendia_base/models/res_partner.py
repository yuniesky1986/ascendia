# -*- coding: utf-8 -*-
# Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api, tools, _
from lxml import etree
from openerp.osv import orm

CERTIFIER_LIST = [('unknown', 'No certification'),
                  ('eqa', 'EQA'),
                  ('applus', 'APPLUS'),
                  ('sgs', 'SGS'),
                  ('aenor', 'AENOR'),
                  ('bureau', 'BUREAU'),
                  ('oca', 'OCA'),
                  ('tuv', 'TUV'),
                  ('bsi', 'BSI'),
                  ('dnv', 'DNV'),
                  ('interconformity', 'Interconformity')]

PARTNER_CLASS_LIST = [('unknown', 'Desconocida'),
                      ('company', 'Company'),
                      ('autonomous', 'Autonomous'),
                      ('public_entity', 'Public Entity'),
                      ('association', 'Association'),
                      ('professional_college', 'Professional College'),
                      ('chamber_commerce', 'Chamber of Commerce'),
                      ('university', 'University')]

PARTNER_SIZE = [('dwarf', 'Dwarf (0-3)'),
                ('micro', 'Micro (4-10)'),
                ('small', 'Small (11-30)'),
                ('medium', 'Medium (31-50)'),
                ('large', 'Large (51-150)'),
                ('large_company', 'Large company (+150)')]


class Partner(models.Model):
    _inherit = 'res.partner'

    # contact fields
    twitter = fields.Char(
        string="Twitter")
    linkedin = fields.Char(
        string="Linkedin")
    facebook = fields.Char(
        string="Facebook")
    last_name = fields.Char(
        string="Last Name")
    alternative_email = fields.Char(
        string="Alternative mail")
    partner_nif = fields.Char(
        string="NIF")
    customer = fields.Boolean(
        string='Is a Customer',
        default=False,
        help="Check this box if this contact is a customer.")
    pqd = fields.Selection(
        [('unknown', 'Unknown'),
         ('yes_pqd', 'Yes PQD'),
         ('no_pqd', 'No PQD')],
        string='PQD',
        default='unknown')
    departament = fields.Many2one(
        'ascendia.department',
        string="Departament")
    ascendia = fields.Many2one(
        'ascendia.ascendia',
        string="Ascendia")
    cnae = fields.Char(
        string="CNAE")

    @api.depends('is_company')
    def _compute_company_type(self):
        for partner in self:
            partner.company_type = 'company' if partner.is_company else 'person'

    company_type = fields.Selection(
        string='Company Type',
        selection=[('person', 'Contact'),
                   ('company', 'Entity')],
        compute='_compute_company_type',
        readonly=False)

    # partner fields
    partner_class = fields.Selection(
        PARTNER_CLASS_LIST,
        string='Class',
        default='unknown')
    activity_sector = fields.Many2one(
        'ascendia.activity.sector',
        string="Activity Sector")
    certifier = fields.Selection(
        CERTIFIER_LIST,
        string='Certifier',
        default='unknown')
    size = fields.Selection(
        PARTNER_SIZE,
        string='Size')
    partner_type = fields.Selection(
        [('public', 'Public'),
         ('private', 'Private')])

    @api.model
    def fields_view_get(self, view_id=None, view_type=False, toolbar=False,
                        submenu=False):
        res = super(Partner, self).fields_view_get(view_id=view_id,
                                                   view_type=view_type,
                                                   toolbar=toolbar,
                                                   submenu=submenu)
        if view_type == 'form':
            doc = etree.XML(res['arch'])
            for node in doc.xpath("//field[@name='customer']"):
                node.set('readonly', "True")
                orm.setup_modifiers(node, None, context=self.env.context,
                                    in_tree_view=False)
            for node in doc.xpath("//field[@name='supplier']"):
                node.set('readonly', "True")
                orm.setup_modifiers(node, None, context=self.env.context,
                                    in_tree_view=False)
            res['arch'] = etree.tostring(doc)
        return res


class Company(models.Model):
    _inherit = 'res.company'

    iban = fields.Char(
        string="IBAN")
