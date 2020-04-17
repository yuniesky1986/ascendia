# -*- coding: utf-8 -*-
# Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Ascendia Financial",
    "version": "10.0.1.0.0",
    "category": "Financial",
    "license": "AGPL-3",
    "website": "https://odoo-community.org/",
    'depends': [
        "l10n_es_aeat_mod111",
        "account_financial_report_qweb",
    ],
    "data": [
        'view/account_view.xml',
        'report/report_mod111.xml',
        'report/report_view.xml',
        # 'report/trial_balance_view.xml',
        'report/layouts.xml',

    ],
    "installable": True,
    "auto_install": False,
}
