# -*- coding: utf-8 -*-
# Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api, tools, _
from itertools import groupby
from odoo.exceptions import UserError, ValidationError


class AccountAccount(models.Model):
    _inherit = 'account.account'

    group = fields.Integer(
        string="Group",
        size=4,
        help="Set group for Level 3 or level 4.")

    '''@api.model
    def default_get(self, default_fields):
        res = super(AccountAccount, self).default_get(default_fields)
        all_account = self.env['account.account'].search([])
        last_account = all_account[len(all_account)-1]
        res.update({'code': int(last_account.code)+1})
        return res'''

    @api.onchange('group')
    def onchange_group(self):
        if self.group:
            flag = True
            account_ids = self.env['account.account'].search([])
            if len(str(self.group))== 3:
                for code3, lines3 in groupby(account_ids, lambda l: l.code[0:3]):
                    lines_accounts3 = list(lines3)
                    if int(code3) == self.group:
                        flag = False
                        last_account = lines_accounts3[len(lines_accounts3)-1]
                        self.code = int(last_account.code)+1
            if len(str(self.group))== 4:
                for code4, lines4 in groupby(account_ids, lambda l: l.code[0:4]):
                    lines_accounts4 = list(lines4)
                    if int(code4) == self.group:
                        flag = False
                        last_account = lines_accounts4[len(lines_accounts4)-1]
                        self.code = int(last_account.code)+1
            if flag:
                raise ValidationError(_('Do not exist any account for this Group: %s') % self.group)
