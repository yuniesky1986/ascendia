# -*- coding: utf-8 -*-
# Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Ascendia Remove menu",
    "version": "10.0.1.0.0",
    "author": "Yunesky Del Rio",
    "category": "tools",
    "license": "AGPL-3",
    "website": "https://odoo-community.org/",
    "depends": ["calendar",
                "sale",
                "sales_team",
                "ascendia_training_credits",
                "project"],
    "data": ['views/remove_menu.xml'
    ],
    "installable": True,
    "auto_install": False,
}
