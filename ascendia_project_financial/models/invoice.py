# -*- coding: utf-8 -*-
from odoo import fields, models, api


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    @api.one
    @api.depends('price_unit', 'discount', 'invoice_line_tax_ids', 'quantity',
                 'product_id', 'invoice_id.partner_id',
                 'invoice_id.currency_id', 'invoice_id.company_id',
                 'invoice_id.date_invoice', 'invoice_id.date')
    def _compute_line_price_total(self):
        currency = self.invoice_id and self.invoice_id.currency_id or None
        price = self.price_unit * (1 - (self.discount or 0.0) / 100.0)
        taxes = False
        if self.invoice_line_tax_ids:
            taxes = self.invoice_line_tax_ids.compute_all(price, currency,
                                                          self.quantity,
                                                          product=self.product_id,
                                                          partner=self.invoice_id.partner_id)
        self.line_price_total = taxes[
            'total_included'] if taxes else self.quantity * price

    line_price_total = fields.Monetary(
        string='Total Amount',
        store=True,
        readonly=True,
        compute='_compute_line_price_total'
    )


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    @api.one
    def _get_invoice_number(self):
        self.invoice_number = ', '.join(inv.number for inv in self.invoice_ids)

    invoice_number = fields.Char(
        string="Invoices",
        compute='_get_invoice_number'
    )