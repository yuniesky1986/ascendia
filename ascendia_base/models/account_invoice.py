# -*- coding: utf-8 -*-
# Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, tools, _
from lxml import etree
from openerp.osv import orm


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    data_protection = fields.Boolean(
        string="Data Protection")

    @api.model
    def fields_view_get(self, view_id=None, view_type=False, toolbar=False,
                        submenu=False):
        res = super(AccountInvoice, self).fields_view_get(view_id=view_id,
                                                          view_type=view_type,
                                                          toolbar=toolbar,
                                                          submenu=submenu)
        if view_type in ('tree', 'form'):
            if self._context.get('type') in ('out_invoice', 'out_refund'):
                state_list = [('draft', _('Draft')),
                              ('proforma', _('Pro-forma')),
                              ('proforma2', _('Pro-forma')),
                              ('open', _('Open')),
                              ('paid', _('Receipt')),
                              ('cancel', _('Cancelled'))]
            else:
                state_list = [('draft', _('Draft1')),
                              ('proforma', _('Pro-forma')),
                              ('proforma2', _('Pro-forma')),
                              ('open', _('Open1')),
                              ('paid', _('Paid')),
                              ('cancel', _('Cancelled'))]
            doc = etree.XML(res['arch'])
            res['fields']['state']['selection'] = state_list
            res['arch'] = etree.tostring(doc)
        return res

    _sql_constraints = [
        ('number_uniq', 'unique(number, company_id, journal_id, type, partner_id)', 'Invoice Number must be unique per Company and Partner!'),
    ]


class AccountAccount(models.Model):
    _inherit = 'account.account'

    @api.model
    def default_get(self, field_list):
        res = super(AccountAccount, self).default_get(field_list)
        if res.get('code', False):
            ag = self.env['account.group']
            code = res.get('code')
            group_id = ag.search([('code_prefix', '=', code[:5])], limit=1)
            if not group_id:
                group_id = ag.search([('code_prefix', '=', code[:4])], limit=1)
                if not group_id:
                    group_id = ag.search([('code_prefix', '=', code[:3])],
                                         limit=1)
            if group_id:
                res['group_id'] = group_id.id
                account_ids = self.search([('group_id', '=', group_id.id),
                                           ('code', 'like', code[:5] + '%')],
                                          order='code DESC')
                if account_ids:
                    res['reconcile'] = account_ids[0].reconcile
                    res['internal_type'] = account_ids[0].internal_type
                    res['user_type_id'] = account_ids[0].user_type_id.id
                    try:
                        res['code'] = str(int(account_ids[0].code) + 1)
                    except:
                        pass
        return res
