# -*- coding: utf-8 -*-
# Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Ascendia CRM Lead Name",
    "version": "10.0.1.0.0",
    "author": "Yunesky Del Rio",
    "category": "CRM",
    "license": "AGPL-3",
    "website": "https://odoo-community.org/",
    "depends": ["crm",
                "ascendia_business_area",
                "ascendia_crm_project"],
    "data": ['views/crm_lead_view.xml'],
    "installable": True,
    "auto_install": False,
}
