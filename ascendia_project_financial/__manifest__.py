# -*- coding: utf-8 -*-
# Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Ascendia Project Financial",
    "version": "10.0.1.0.0",
    "author": "Yunesky Del Rio",
    "category": "Project",
    "license": "AGPL-3",
    "website": "https://odoo-community.org/",
    "depends": ["ascendia_project",
                "ascendia_crm_project",
                "project",
                "hr_timesheet",
                "sale_timesheet"],
    "data": ['views/payment_view.xml',
             'views/account_view.xml',
             'views/purchase_view.xml',
             'views/sale_order_view.xml',
             'views/project_view.xml',
             'views/res_config_settings_views.xml'],
    "installable": True,
    "auto_install": False,
}
