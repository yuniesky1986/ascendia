import datetime

from odoo import fields, models, api, _, tools
from odoo.exceptions import ValidationError

ALERT_STATES = [
    ('no_alert', 'No Alert'),
    ('alert_25', 'Alert 25 days'),
    ('alert_45', 'Alert 45 days'),
]


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    payment_alert_state = fields.Selection(ALERT_STATES, 'Alert State',
                                           readonly=True,
                                           default=lambda *a: 'no_alert')
    url = fields.Char(compute='_compute_url')

    @api.one
    def send_email(self, tpl='ascendia_invoice_payment.email_payment_25'):
        template = self.env.ref(tpl, False)
        if template:
            template.sudo().send_mail(self.id)

    @api.model
    def payment_monitoring(self, autocommit=False):
        invoices = self.search([
            ('state', '=', 'open'),
            ('type', '=', 'out_invoice'),
            ('payment_alert_state', 'in', ['no_alert']),
            ('date_invoice', '<=',
             datetime.datetime.strftime(
                 fields.datetime.now() - datetime.timedelta(days=25),
             tools.DEFAULT_SERVER_DATE_FORMAT))
        ])
        for invoice in invoices:
            if invoice.payment_alert_state == 'no_alert':
                invoice.send_email()
                invoice.payment_alert_state = 'alert_25'

    def payment_monitoring_45(self, autocommit=False):
        invoices = self.search([
            ('state', '=', 'open'),
            ('type', '=', 'out_invoice'),
            ('payment_alert_state', 'in', ['alert_25', 'no_alert']),
            ('date_invoice', '<=',
             datetime.datetime.strftime(
                 fields.datetime.now() - datetime.timedelta(days=45),
                 tools.DEFAULT_SERVER_DATE_FORMAT))
        ])
        for invoice in invoices:
            if invoice.payment_alert_state in ['alert_25', 'no_alert']:
                invoice.send_email('ascendia_invoice_payment.email_payment_45')
                invoice.payment_alert_state = 'alert_45'

    def _compute_url(self):
        server = self.env['ir.config_parameter'].get_param('web.base.url')
        if self.type in ['in_invoice', 'in_refund']:
            menu = self.env['ir.model.data'].xmlid_to_res_id(
                'account.menu_action_invoice_tree2')
            action = self.env['ir.model.data'].xmlid_to_res_id(
                'account.action_invoice_tree2')
        else:
            menu = self.env['ir.model.data'].xmlid_to_res_id(
                'account.menu_action_invoice_tree2')
            action = self.env['ir.model.data'].xmlid_to_res_id(
                'account.action_invoice_tree1')
        url = "%s/web#id=%s&view_type=form" \
              "&model=account.invoice" \
              "&menu_id=%s&action=%s" \
              % (server, self.id, menu, action)
        self.url = url

    def due_date_monitoring(self, autocommit=False):
        invoices = self.search([
            ('state', '=', 'draft'),
            ('date_invoice', '<=',
             datetime.datetime.strftime(
                 fields.datetime.now() + datetime.timedelta(days=3),
                 tools.DEFAULT_SERVER_DATE_FORMAT))
        ])
        for invoice in invoices:
            invoice.send_email('ascendia_invoice_payment.email_due_date_invoice')
