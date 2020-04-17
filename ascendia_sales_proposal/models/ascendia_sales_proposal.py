# -*- coding: utf-8 -*-
from odoo import fields, models, api,_
from odoo.exceptions import ValidationError


PROPOSAL_SATES = [
    ('draft', 'Draft'),
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('out_of_date', 'Out of Date'),
    ('cancel', 'Cancel')
]


class EconomicCondition(models.Model):
    _name = 'ascendia.economic.condition'

    text = fields.Text('Concept')
    amount = fields.Float('Amount')
    proposal_id = fields.Many2one('ascendia.sale.proposal')


class SaleProposal(models.Model):
    _name = 'ascendia.sale.proposal'

    name = fields.Char("Name")
    private_state = fields.Selection(PROPOSAL_SATES, 'State',
                             default='draft')
    state = fields.Selection(PROPOSAL_SATES, 'State',
                             readonly=True,
                             compute='_compute_state',
                             inverse='_set_state',
                             default=lambda *a: 'draft')
    is_out_date = fields.Boolean('Is out of date',
                                 compute='_compute_out_date')
    request_date = fields.Date("Due Date")
    approval_date = fields.Date("Approval Date")
    import_template_id = fields.Many2one('ascendia.sale.proposal',
                                         'Import Template')
    partner_id = fields.Many2one('res.partner', 'Partner')
    contact_id = fields.Many2one('res.partner', 'Contact')
    company_type = fields.Selection(related='partner_id.company_type', string='Company Type')
    # contact_ids = fields.Many2many('res.partner',
    #                                'rel_proposal_contact',
    #                                'proposal_id',
    #                                'contact_id',
    #                                'Contacts')
    sale_order_ids = fields.One2many('sale.order',
                                     'proposal_id',
                                     'Sale Orders')

    make_by = fields.Many2one('res.users', 'Make By',
                              default=lambda a: a.env.user)
    revised_by = fields.Many2one('res.users', 'Revised by')

    legal_text = fields.Html('Legal text')
    objective = fields.Html('Legal text')
    economic_condition = fields.One2many('ascendia.economic.condition',
                                         'proposal_id',
                                         'Economic Conditions')
    include_iva = fields.Boolean('Include IVA')
    include_outcome = fields.Boolean('Include Outcome')
    valid_date = fields.Date('Valid Date')
    payment_way = fields.Html('Payment Way')

    @api.one
    def _compute_out_date(self):
        if self.request_date < fields.Date.context_today(self):
            self.is_out_date = True
        else:
            self.is_out_date = False

    @api.one
    def _compute_state(self):
        if self.is_out_date:
            if self.private_state == 'approved':
                self.state = 'out_of_date'
                self.private_state = 'out_of_date'
            else:
                self.state = self.private_state
        else:
            self.state = self.private_state

    @api.one
    def _set_state(self):
        if self.state == 'out_of_date' and \
                        self.private_state in ['draft', 'out_of_date']:
            return
        self.private_state = self.state

    @api.multi
    def _get_date(self):
        date = fields.Datetime.now()
        months = [_('Enero'),_('Febrero'),_('Marzo'),_('Abril'),_('Mayo'),_('Junio'),_('Julio'),_('Agosto'),_('Septiembre'),_('Octubre'),_('Noviembre'),_('Diciembre')]
        parts = date.split('-')
        day = str(parts[2]).split(' ')[0]
        pos = int(parts[1])
        month= months[pos-1]
        cadena = 'En Sevilla, a '+ (day) + ' de ' + str(month) + ' de ' + parts[0]
        return cadena

    @api.multi
    def _get_website(self):
        website = self.make_by.company_id.partner_id.website
        if website:
            parts = website.split('//')
            if len(parts)>= 2:
                website = parts[1].upper()
        return website

    @api.multi
    def _get_email(self):
        email = self.make_by.company_id.partner_id.email
        if email:
            email = email.upper()
        return email

    @api.multi
    def _get_other_part_name(self):
        name = ''
        if self.partner_id:
            if self.partner_id.child_ids:
                for element in self.partner_id.child_ids:
                    if element.function.lower() == 'gerente':
                        if element.name:
                            name = element.name
                        if element.last_name:
                            name += element.last_name
                        break
        cadena = name
        return cadena

    @api.multi
    def _get_other_part_contact_name(self):
        name = ''
        if self.contact_id:
            if self.contact_id.name:
                name = self.contact_id.name.name
            if self.contact_id.last_name:
                name += ' ' + self.contact_id.last_name

        cadena = name
        return cadena

    @api.multi
    def _get_other_part_dni(self):
        dni = ''
        if self.partner_id:
            if self.partner_id.child_ids:
                for element in self.partner_id.child_ids:
                    if element.function.lower() == 'gerente':
                        if element.dni:
                            dni = element.dni
                        break
        cadena = dni
        return cadena

    @api.multi
    def _get_other_part_street(self):
        street = ''
        if self.partner_id:
            if self.partner_id.street:
                street = self.partner_id.street
        cadena = street
        return cadena

    @api.multi
    def _get_total_amount_untaxed(self):
        total = 0.0
        if self.sale_order_ids:
            for element in self.sale_order_ids:
                if element.amount_untaxed:
                    total += element.amount_untaxed
        cadena = str(total)
        return cadena
    
    @api.multi
    def _get_total_economic_cond(self):
        return sum(self.economic_condition.mapped('amount'))

    @api.multi
    def _get_approval_date(self):
        cadena = ''
        if self.approval_date:
            date = self.approval_date
            months = [_('Enero'),_('Febrero'),_('Marzo'),_('Abril'),_('Mayo'),_('Junio'),_('Julio'),_('Agosto'),_('Septiembre'),_('Octubre'),_('Noviembre'),_('Diciembre')]
            parts = date.split('-')
            day = str(parts[2]).split(' ')[0]
            pos = int(parts[1])
            month= months[pos-1]
            cadena = (day) + ' de ' + str(month) + ' de ' + parts[0]
        return cadena

    @api.multi
    def _get_request_date(self):
        cadena = ''
        if self.request_date:
            date = self.request_date
            months = [_('Enero'),_('Febrero'),_('Marzo'),_('Abril'),_('Mayo'),_('Junio'),_('Julio'),_('Agosto'),_('Septiembre'),_('Octubre'),_('Noviembre'),_('Diciembre')]
            parts = date.split('-')
            day = str(parts[2]).split(' ')[0]
            pos = int(parts[1])
            month= months[pos-1]
            cadena = (day) + ' de ' + str(month) + ' de ' + parts[0]
        return cadena

    @api.onchange('is_out_date')
    def onchange_is_out_date(self):
        self.state = 'out_of_date'

    @api.onchange('import_template_id')
    def onchange_import_template_id(self):
        if self.import_template_id:
            self.legal_text = self.import_template_id.legal_text
            self.objective = self.import_template_id.objective
            self.payment_way = self.import_template_id.payment_way

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        self.revised_by = self.partner_id.user_id

    @api.one
    def action_draft(self):
        self.state = 'draft'

    @api.one
    def action_pending(self):
        self.state = 'pending'

    @api.one
    def action_approved(self):
        self.state = 'approved'
        if not self.approval_date:
            self.approval_date = fields.Date.context_today(self)

    @api.one
    def action_cancel(self):
        self.state = 'cancel'
