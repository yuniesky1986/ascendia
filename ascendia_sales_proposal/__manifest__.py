# -*- coding: utf-8 -*-
# Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Ascendia Sales Proposal",
    "version": "10.0.1.0.0",
    "author": "Rembero Loanny",
    "category": "Sale",
    "license": "AGPL-3",
    "website": "https://odoo-community.org/",
    "depends": ["ascendia_base", "sale"],
    "data": [
        'security/ir.model.access.csv',
        'views/report_proposal.xml',
        'views/ascendia_sales_proposal.xml',
        'views/sale_order_view.xml',
        'views/res_partner_view.xml',
    ],
    "installable": True,
    "auto_install": False,
}
