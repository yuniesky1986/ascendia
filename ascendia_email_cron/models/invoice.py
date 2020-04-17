# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010, 2014 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api, _
from datetime import datetime


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    pending_to_pay = fields.Boolean()
    email_send = fields.Boolean()

    @api.model
    def _cron_pending_to_receive_invoice(self):
        model_data = self.env['ir.model.data']
        template_id = model_data.get_object_reference('ascendia_email_cron',
                                                      'email_template_notify_customer_invoice')[1]
        email_template = self.env['mail.template'].browse(template_id)
        today = datetime.today()
        for aux in self.search([('email_send', '=', False),
                                ('type', 'in', ['out_invoice', 'out_refund']),
                                ('state', '=', 'open')]):
            if aux.date_due:
                date_due = datetime.strptime(aux.date_due, '%Y-%m-%d')
                if (today - date_due).days >= 15:
                    aux.email_send = True
                    email_template.send_mail(res_id=aux.id, force_send=True)

    @api.model
    def _cron_pending_to_payment_invoice(self):
        today = datetime.today()
        for aux in self.search([('type', 'in', ['in_invoice', 'in_refund']),
                                ('state', '=', 'open')]):
            if aux.date_due:
                date_due = datetime.strptime(aux.date_due, '%Y-%m-%d')
                if (date_due - today).days <= 10:
                    aux.pending_to_pay = True

    @api.model
    def create(self, vals):
        res = super(AccountInvoice, self).create(vals)
        today = datetime.today()
        if res.date_due:
            date_due = datetime.strptime(res.date_due, '%Y-%m-%d')
            if (date_due - today).days <= 10:
                res.pending_to_pay = True
        return res

    @api.one
    def write(self, vals):
        if vals.get('state') == 'paid':
            vals.update({'pending_to_pay': False})
        if vals.get('date_due'):
            today = datetime.today()
            date_due = datetime.strptime(vals.get('date_due'), '%Y-%m-%d')
            if (date_due - today).days <= 10:
                vals.update({'pending_to_pay': True})
        return super(AccountInvoice, self).write(vals)
