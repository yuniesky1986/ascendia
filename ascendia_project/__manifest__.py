# -*- coding: utf-8 -*-
# Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Ascendia Project",
    "version": "10.0.1.0.0",
    "author": "Yunesky Del Rio",
    "category": "Project",
    "license": "AGPL-3",
    "website": "https://odoo-community.org/",
    "depends": ["project",
                "project_issue",
                "project_issue_sheet",
                "rating_project",
                "ascendia_sales_proposal",
                "ascendia_crm",
                "hr_timesheet"],
    "data": ['data/data.xml',
             'security/ir.model.access.csv',
             'views/project_view.xml',
             'views/proposal_view.xml'],
    "installable": True,
    "auto_install": False,
}
