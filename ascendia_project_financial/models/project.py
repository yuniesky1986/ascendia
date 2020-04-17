# -*- coding: utf-8 -*-
from odoo import fields, models, api


class Project(models.Model):
    _inherit = 'project.project'

    """Incomes"""
    lead_amount = fields.Float(
        related='lead_id.planned_revenue',
        readonly=1
    )

    @api.one
    def _get_sale_total(self):
        sale = self.env['sale.order']
        sale_ids = sale.search([('project_id', '=',
                                 self.analytic_account_id.id),
                                ('state', 'not in', ['draft', 'cancel'])])
        self.sale_total = sum(sale_ids.mapped('amount_total'))
        self.sale_subtotal = sum(sale_ids.mapped('amount_untaxed'))
        self.sales_count = len(sale_ids.mapped('id'))

    sale_total = fields.Float(
        string="Sale Total",
        compute='_get_sale_total',
    )
    sale_subtotal = fields.Float(
        string="Sale Total Without IVA",
        compute='_get_sale_total',
    )
    sales_count = fields.Integer(
        compute='_get_sale_total',
        string='# Sales'
    )

    @api.one
    def _customer_get_state_progress(self):
        line = self.env['account.invoice.line']
        inv_line_ids = line.search([('account_analytic_id', '=',
                                 self.analytic_account_id.id),
                                ('invoice_id.state', 'in', ['open', 'paid']),
                                ('invoice_id.type', '=', 'out_invoice')])
        customer_amount_tax = sum(inv_line_ids.mapped('line_price_total'))
        ref_line_ids = line.search([('account_analytic_id', '=',
                                 self.analytic_account_id.id),
                                ('invoice_id.state', 'in', ['open', 'paid']),
                                ('invoice_id.type', '=', 'out_refund')])
        refund_amount_tax = sum(ref_line_ids.mapped('line_price_total'))
        amount_tax = customer_amount_tax - refund_amount_tax
        if self.sale_total:
            self.progress_invoiced = amount_tax * 100 / (self.sale_total or 1)
        elif amount_tax:
            self.progress_invoiced = 100
        all_invoices = inv_line_ids + ref_line_ids
        if all_invoices:
            pay_ids = all_invoices.mapped('invoice_id').mapped('payment_ids')
            if pay_ids:
                amount = sum(pay_ids.mapped('amount'))
                self.progress_paid = amount * 100 / (amount_tax or 1)
                self.customer_pay_count = len(pay_ids)
        self.customer_invoice_count = len(all_invoices)

    progress_invoiced = fields.Float(
        string="Invoice Progress",
        readonly=True,
        compute='_customer_get_state_progress')
    progress_paid = fields.Float(
        string="Received State",
        readonly=True,
        compute='_customer_get_state_progress')
    customer_invoice_count = fields.Integer(
        compute='_customer_get_state_progress',
        string='# Invoices'
    )
    customer_pay_count = fields.Integer(
        compute='_customer_get_state_progress',
        string='# Payments'
    )

    """Outcomes"""

    @api.one
    def get_timesheet_total(self):
        analytic_line = self.env['account.analytic.line']
        lines = analytic_line.search([('project_id', '=', self.id)])
        timesheet_total = sum(lines.mapped('amount'))
        if timesheet_total < 0:
            timesheet_total *= -1
        self.timesheet_total = timesheet_total

    timesheet_total = fields.Float(
        string="Timesheet Total",
        compute='get_timesheet_total'
    )
    @api.one
    def _get_purchase_total(self):
        purchase = self.env['purchase.order.line']
        purchase_ids = purchase.search([('account_analytic_id', '=',
                                         self.analytic_account_id.id),
                                        ('order_id.state', 'not in',
                                         ['draft', 'cancel'])])
        self.purchase_total = sum(purchase_ids.mapped('price_total'))
        self.purchase_subtotal = sum(purchase_ids.mapped('price_subtotal'))
        self.purchase_count = len(purchase_ids.mapped('id'))

    purchase_total = fields.Float(
        string="Purchase Total",
        compute='_get_purchase_total',
    )
    purchase_subtotal = fields.Float(
        string="Purchase Total Without IVA",
        compute='_get_purchase_total',
    )
    purchase_count = fields.Integer(
        compute='_get_purchase_total',
        string='# Purchases'
    )

    @api.one
    def _supplier_get_state_progress(self):
        line = self.env['account.invoice.line']
        sup_line_ids = line.search([('account_analytic_id', '=',
                                     self.analytic_account_id.id),
                                    ('invoice_id.state', 'in', ['open', 'paid']),
                                    ('invoice_id.type', '=', 'in_invoice')])
        customer_amount_tax = sum(sup_line_ids.mapped('line_price_total'))
        ref_line_ids = line.search([('account_analytic_id', '=',
                                 self.analytic_account_id.id),
                                ('invoice_id.state', 'in', ['open', 'paid']),
                                ('invoice_id.type', '=', 'in_refund')])
        refund_amount_tax = sum(ref_line_ids.mapped('line_price_total'))
        amount_tax = customer_amount_tax - refund_amount_tax
        if self.purchase_total:
            self.sup_progress_invoiced = amount_tax * 100 / (self.purchase_total or 1)
        elif amount_tax:
            self.sup_progress_invoiced = 100
        all_invoices = sup_line_ids + ref_line_ids
        if all_invoices:
            pay_ids = all_invoices.mapped('invoice_id').mapped('payment_ids')
            if pay_ids:
                amount = sum(pay_ids.mapped('amount'))
                self.sup_progress_paid = amount * 100 / (amount_tax or 1)
                self.supplier_pay_count = len(pay_ids)
            self.supplier_invoice_count = len(all_invoices)

    sup_progress_invoiced = fields.Float(
        string="Supplier Invoice",
        readonly=True,
        compute='_supplier_get_state_progress')
    sup_progress_paid = fields.Float(
        string="Paid State",
        readonly=True,
        compute='_supplier_get_state_progress'
    )
    supplier_invoice_count = fields.Integer(
        compute='_supplier_get_state_progress',
        string='# Invoices'
    )
    supplier_pay_count = fields.Integer(
        compute='_supplier_get_state_progress',
        string='# Payments'
    )

    @api.multi
    def action_view_sales(self):
        self.ensure_one()
        action = self.env.ref(
            'ascendia_project_financial.action_orders_financial_supplier')
        result = action.read()[0]
        result['domain'] = [('project_id', '=', self.analytic_account_id.id),
                            ('state', 'not in', ['draft', 'cancel'])]
        return result

    @api.multi
    def action_view_invoice_customer(self):
        self.ensure_one()
        action = self.env.ref(
            'ascendia_project_financial.action_view_invoice_line_tree_financial_project')
        result = action.read()[0]
        result['domain'] = [('account_analytic_id', '=',
                             self.analytic_account_id.id),
                            ('invoice_id.state', 'in', ['open', 'paid']),
                            ('invoice_id.type', 'in',
                             ['out_invoice', 'out_refund'])]
        return result

    @api.multi
    def action_view_paid_customer(self):
        self.ensure_one()
        line = self.env['account.invoice.line']
        inv_line_ids = line.search([('account_analytic_id', '=',
                                     self.analytic_account_id.id),
                                    ('invoice_id.state', 'in',
                                     ['open', 'paid']),
                                    ('invoice_id.type', 'in',
                                     ['out_invoice', 'out_refund'])])
        pay_ids = inv_line_ids.mapped('invoice_id').mapped('payment_ids')
        action = self.env.ref(
            'ascendia_project_financial.action_account_payments_financial_customer')
        result = action.read()[0]
        result['domain'] = [('id', 'in', pay_ids.mapped('id')),
                            ('partner_type', '=', 'customer')]
        return result

    @api.multi
    def action_view_purchases(self):
        self.ensure_one()
        action = self.env.ref(
            'ascendia_project_financial.action_financial_project')
        result = action.read()[0]
        result['domain'] = [('account_analytic_id', '=',
                             self.analytic_account_id.id),
                            ('order_id.state', 'not in', ['draft', 'cancel'])]
        return result

    @api.multi
    def action_view_invoice_supplier(self):
        self.ensure_one()
        action = self.env.ref(
            'ascendia_project_financial.action_view_invoice_line_tree_financial_project')
        result = action.read()[0]
        result['domain'] = [('account_analytic_id', '=',
                             self.analytic_account_id.id),
                            ('invoice_id.state', 'in', ['open', 'paid']),
                            ('invoice_id.type', 'in',
                             ['in_invoice', 'in_refund'])]
        return result

    @api.multi
    def action_view_paid_supplier(self):
        self.ensure_one()
        line = self.env['account.invoice.line']
        inv_line_ids = line.search([('account_analytic_id', '=',
                                     self.analytic_account_id.id),
                                    ('invoice_id.state', 'in',
                                     ['open', 'paid']),
                                    ('invoice_id.type', 'in',
                                     ['in_invoice', 'in_refund'])])
        pay_ids = inv_line_ids.mapped('invoice_id').mapped('payment_ids')
        action = self.env.ref(
            'ascendia_project_financial.action_account_payments_financial_supplier')
        result = action.read()[0]
        result['domain'] = [('id', 'in', pay_ids.mapped('id')),
                            ('partner_type', '=', 'supplier')]
        return result

    @api.multi
    def account_analytic_line_action_financial(self):
        self.ensure_one()
        action = self.env.ref(
            'ascendia_project_financial.action_analytic_line_tree'
        )
        result = action.read()[0]
        result['domain'] = [('account_id', '=', self.analytic_account_id.id)]
        return result
