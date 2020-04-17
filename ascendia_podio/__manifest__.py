# -*- coding: utf-8 -*-
# Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Ascendia Podio",
    "version": "10.0.1.0.0",
    "author": "Whitebite",
    "category": "Whitebite",
    "license": "AGPL-3",
    "website": "https://odoo-community.org/",
    "depends": ["base",
                "document",
                "project",
                "crm"
                ],
    "data": [
            'security/ir.model.access.csv',
            'data/data.xml',
            'views/menu_view.xml',
            'views/city_view.xml',
            'views/course_view.xml',
            'views/student_view.xml',
            'views/marketing_view.xml',
            'views/baremation_view.xml',
            'views/certificate_view.xml',
            ],
    "installable": True,
    "auto_install": False,
}
