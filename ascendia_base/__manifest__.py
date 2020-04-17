# -*- coding: utf-8 -*-
# Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Ascendia Base",
    "version": "10.0.1.0.0",
    "author": "Rembero Loanny",
    "category": "Sale",
    "license": "AGPL-3",
    "website": "https://odoo-community.org/",
    "depends": ["base",
                "sales_team",
                "mail",
                "account",
                "account_invoice_currency",
                "report",
                "l10n_es_account_invoice_sequence",
                "purchase"],
    "data": ['views/account_invoice.xml',
             'views/res_partner.xml',
             'views/activity_sector.xml',
             'security/ir.model.access.csv',
             'report/report_invoice.xml',
             'views/purchase_order.xml'
    ],
    "installable": True,
    "auto_install": False,
}
