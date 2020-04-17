# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    parent_id = fields.Many2one(
        comodel_name='account.analytic.account',
        string='Analytic Account Parent',
        related='account_id.parent_id',
        store=True
    )
    tag_id = fields.Many2one(
        comodel_name='account.analytic.tag',
        string='Tag',
        compute='_compute_principal_tag',
        store=True
    )
    balance = fields.Monetary(
        compute='_compute_debit_credit_balance',
        string='Balance',
        store=True
    )
    debit = fields.Monetary(
        compute='_compute_debit_credit_balance',
        string='Debit',
        store=True
    )
    credit = fields.Monetary(
        compute='_compute_debit_credit_balance',
        string='Credit',
        store=True
    )

    @api.multi
    @api.depends('account_id')
    def _compute_principal_tag(self):
        for account in self:
            tag_id = \
                account.account_id.tag_ids and account.account_id.tag_ids[0]
            if not tag_id and account.account_id.parent_id:
                tag_id = \
                    account.account_id.parent_id.tag_ids and \
                    account.account_id.parent_id.tag_ids[0]
            account.tag_id = tag_id.id

    @api.multi
    @api.depends('amount')
    def _compute_debit_credit_balance(self):
        for account in self:
            account.debit = account.amount < 0.0 and abs(account.amount) or 0.0
            account.credit = account.amount > 0.0 and account.amount or 0.0
            account.balance = account.credit - account.debit


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    @api.multi
    def _compute_debit_credit_balance(self):
        super(AccountAnalyticAccount, self)._compute_debit_credit_balance()
        for account in self:
            account.debit = abs(account.debit)
            account.balance = account.credit - account.debit
