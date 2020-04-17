from odoo import models, fields, api
from datetime import date
from lxml import etree
from openerp.osv import orm

ORIGIN_LIST = [('tracking', 'Commercial Tracking'),
               ('commission', 'Appointed by Contributor (Commission)'),
               ('appointed', 'Appointed by Contributor'),
               ('targeted_client', 'Targeted by the Own Client'),
               ('targeted_technician', 'Targeted by the Technician'),
               ('incoming', 'Incoming / Web Call'),
               ('follow', 'Follow-up by RRC'),
               ('others', 'Others')]

FINANCING_LIST = [('tripartite',
                   'Tripartite Foundation - Fundae (Government of Spain)'),
                  ('without', 'Without help'),
                  ('innocamaras', 'Innocamaras (Chamber of Commerce)'),
                  ('ecoinnocamaras', 'Ecoinnocamaras (Chamber of Commerce)'),
                  ('idea', 'Idea Agency (Junta de Andalucia)'),
                  ('government', 'Government of Spain'),
                  ('tic', 'Tic Chambers (Chamber of Commerce)'),
                  ('redes', 'Red.es (Government of Spain)'),
                  ('ministry',
                   'Ministry of the Presidency of the Junta de Andalucia (Junta de Andalucia)'),
                  ('neotec', 'Neotec (Government of Spain)'),
                  ('check', 'Check Innovation (Junta de Andalucia)'),
                  ('department',
                   'Department of Employment, Business and Commerce (Junta de Andalucia)')]


class CRMCharge(models.Model):
    _name = 'crm.charge'
    _order = 'name'

    name = fields.Char(
        string="Name")
    tag_ids = fields.Many2many(
        'crm.lead.tag',
        string="Tags")


class CRMLead(models.Model):
    _inherit = 'crm.lead'

    can_be_create = fields.Boolean(
        string="Can be create Price Request",
        related='stage_id.can_be_create')
    close_date = fields.Date(
        string="Close Date")
    request_id = fields.Many2one(
        'ascendia.price.request',
        string="Price Request Name")
    request_date = fields.Date(
        string="Date",
        related='request_id.request_date')
    total_sale = fields.Float(
        string='Total Sale Price',
        related='request_id.total_sale')
    total_purchase = fields.Float(
        string='Total Purchase Price',
        related='request_id.total_purchase')
    total_gain = fields.Float(
        string='Total Gain',
        related='request_id.total_gain')
    state = fields.Selection(
        [('open', 'Open'),
         ('won', 'Won'),
         ('lost', 'Lost')],
        string="State",
        default='open')
    contact_id = fields.Many2one(
        'res.partner',
        string="Contact")
    charge_id = fields.Many2one(
        'crm.charge',
        string="Charge")
    technical_ids = fields.Many2many(
        'res.users',
        string='technical')
    origin = fields.Selection(
        ORIGIN_LIST,
        string='Origin')
    technical_price = fields.Float(
        string="Technical Price")
    start_date = fields.Date(
        string="Start Date")
    financing = fields.Selection(
        FINANCING_LIST,
        string='Financing')
    opt_out = fields.Boolean(
        string='Opt-Out',
        oldname='optout',
        default=True,
        help="If opt-out is checked, this contact has refused to receive emails for mass mailing and marketing campaign. "
             "Filter 'Available for Mass Mailing' allows users to filter the leads when performing mass mailing.")

    @api.onchange('partner_id')
    def onchange_partner(self):
        self.contact_ids = False

    @api.onchange('contact_id')
    def _onchange_contact_id(self):
        if self.contact_id:
            self.contact_name = self.contact_id.name
            self.title = self.contact_id.title
            self.function = self.contact_id.function
            self.mobile = self.contact_id.mobile
            self.fax = self.contact_id.fax

    @api.one
    def action_create_price_request(self):
        if self.partner_id:
            vals = {'client_id': self.partner_id.id,
                    'responsible_id': self.user_id.id,
                    'request_date': date.today()}
            request = self.env['ascendia.price.request']
            self.request_id = request.create(vals).id

    @api.multi
    def action_set_won(self):
        for lead in self:
            lead.write({'state': 'won', 'probability': 100})
        return True

    @api.multi
    def action_set_lost(self):
        for lead in self:
            lead.write({'probability': 0, 'state': 'lost'})  # 'active': False
        return True

    @api.multi
    def action_set_open(self):
        for lead in self:
            stage_id = lead._stage_find(domain=[])
            lead.write({'state': 'open', 'active': True,
                        'stage_id': stage_id.id, 'probability': 0})
        return True

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        values = {}
        if self.partner_id:
            values = self._onchange_partner_id_values(self.partner_id.id)
            contact_name = self.partner_id.name
            if self.partner_id.is_company and self.partner_id.child_ids:
                contact_name = self.partner_id.child_ids[0].name
            values.update({'contact_name': contact_name})
        self.update(values)

    @api.model
    def fields_view_get(self, view_id=None, view_type=False, toolbar=False,
                        submenu=False):
        res = super(CRMLead, self).fields_view_get(view_id=view_id,
                                                   view_type=view_type,
                                                   toolbar=toolbar,
                                                   submenu=submenu)
        if view_type == 'form':
            doc = etree.XML(res['arch'])
            pages = doc.xpath("//page")
            if pages:
                pages[0].set('invisible', "True")
                orm.setup_modifiers(pages[0], None, context=self.env.context,
                                    in_tree_view=False)
            res['arch'] = etree.tostring(doc)
        return res
