# -*- coding: utf-8 -*-
# © 2016 Julien Coux (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api
from itertools import groupby


class TrialBalanceReport(models.TransientModel):
    _inherit = 'report_trial_balance_qweb'

    @api.model
    def _get_report_values(self):
        result = []
        account_trial_balance_ids = self.env['report_trial_balance_qweb_account'].search([])

        for code3, lines3 in groupby(account_trial_balance_ids, lambda l: l.code[0:3]):
            lines_accounts3 = list(lines3)
            total_initial_balance_level3 = 0
            total_debit_level3 = 0
            total_credit_level3 = 0
            total_final_balance_level3 = 0
            total_initial_balance_foreign_currency_level3 = 0
            total_final_balance_foreign_currency_level3 = 0
            currency = ''

            for code4, lines4 in groupby(lines_accounts3, lambda l: l.code[0:4]):
                lines_accounts4 = list(lines4)
                total_initial_balance_level4 = 0
                total_debit_level4 = 0
                total_credit_level4 = 0
                total_final_balance_level4 = 0
                total_initial_balance_foreign_currency_level4 = 0
                total_final_balance_foreign_currency_level4 = 0

                for account in lines_accounts4:
                    total_initial_balance_level4 += account.initial_balance
                    total_debit_level4 += account.debit
                    total_credit_level4 += account.credit
                    total_final_balance_level4 += account.final_balance
                    total_initial_balance_foreign_currency_level4 += account.initial_balance_foreign_currency
                    total_final_balance_foreign_currency_level4 += account.final_balance_foreign_currency
                    if account.currency_id:
                        currency = account.currency_id.name
                    result.append({'code': account.code, 'name': account.name, 'initial_balance': account.initial_balance, 'debit': account.debit, 'credit': account.credit, 'final_balance': account.final_balance, 'initial_balance_foreign_currency': account.initial_balance_foreign_currency, 'final_balance_foreign_currency': account.final_balance_foreign_currency, 'currency': currency})

                result.append({'code': code4 + '*****', 'name': 'Total grupo ' + code4, 'initial_balance': total_initial_balance_level4, 'debit': total_debit_level4, 'credit': total_credit_level4, 'final_balance': total_final_balance_level4, 'initial_balance_foreign_currency': total_initial_balance_foreign_currency_level4, 'final_balance_foreign_currency': total_final_balance_foreign_currency_level4, 'currency': currency})

                total_initial_balance_level3 += total_initial_balance_level4
                total_debit_level3 += total_debit_level4
                total_credit_level3 += total_credit_level4
                total_final_balance_level3 += total_final_balance_level4
                total_initial_balance_foreign_currency_level3 += total_initial_balance_foreign_currency_level4
                total_final_balance_foreign_currency_level3 += total_final_balance_foreign_currency_level4

            result.append({'code': code3 + '******', 'name': 'Total grupo ' + code3, 'initial_balance': total_initial_balance_level3, 'debit': total_debit_level3, 'credit': total_credit_level3, 'final_balance': total_final_balance_level3, 'initial_balance_foreign_currency': total_initial_balance_foreign_currency_level3, 'final_balance_foreign_currency': total_final_balance_foreign_currency_level3, 'currency': currency})
        return result

#     def _inject_account_values(self, account_ids):
#         """Inject report values for report_trial_balance_qweb_account"""
#         sql = (
#             "DELETE FROM report_trial_balance_qweb_account"
#         )
#         cr = self.env.cr
#         cr.execute(sql)
#         query_inject_account = """
# INSERT INTO
#     report_trial_balance_qweb_account
#     (
#     report_id,
#     create_uid,
#     create_date,
#     account_id,
#     code,
#     name,
#     initial_balance,
#     debit,
#     credit,
#     final_balance,
#     currency_id,
#     initial_balance_foreign_currency,
#     final_balance_foreign_currency
#     )
# SELECT
#     %s AS report_id,
#     %s AS create_uid,
#     NOW() AS create_date,
#     acc.id,
#     acc.code,
#     acc.name,
#     coalesce(rag.initial_balance, 0) AS initial_balance,
#     coalesce(rag.final_debit - rag.initial_debit, 0) AS debit,
#     coalesce(rag.final_credit - rag.initial_credit, 0) AS credit,
#     coalesce(rag.final_balance, 0) AS final_balance,
#     rag.currency_id AS currency_id,
#     coalesce(rag.initial_balance_foreign_currency, 0)
#         AS initial_balance_foreign_currency,
#     coalesce(rag.final_balance_foreign_currency, 0)
#         AS final_balance_foreign_currency
# FROM
#     account_account acc
#     LEFT OUTER JOIN report_general_ledger_qweb_account AS rag
#         ON rag.account_id = acc.id AND rag.report_id = %s
# WHERE
#     acc.id in %s
#         """
#         if self.hide_account_balance_at_0:
#             query_inject_account += """ AND
#     final_balance IS NOT NULL AND final_balance != 0"""
#         query_inject_account_params = (
#             self.id,
#             self.env.uid,
#             self.general_ledger_id.id,
#             account_ids._ids,
#         )
#         self.env.cr.execute(query_inject_account, query_inject_account_params)
