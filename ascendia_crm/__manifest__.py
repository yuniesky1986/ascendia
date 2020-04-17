# -*- coding: utf-8 -*-
# Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Ascendia CRM",
    "version": "10.0.1.0.0",
    "author": "Yunesky Del Rio",
    "category": "CRM",
    "license": "AGPL-3",
    "website": "https://odoo-community.org/",
    "depends": ["crm",
                "sale_crm",
                "sales_team",
                "ascendia_price_request"],
    "data": ['security/security.xml',
             'security/ir.model.access.csv',
             'views/delete_view.xml',
             'views/crm_menu_view.xml',
             'views/crm_stage_view.xml',
             'views/crm_lead_view.xml',
             'views/res_partner_view.xml'],
    "installable": True,
    "auto_install": False,
}
