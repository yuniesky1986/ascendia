# -*- coding: utf-8 -*-
# Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Ascendia Training Credits",
    "version": "10.0.1.0.0",
    "author": "Yunesky Del Rio",
    "category": "Sale",
    "license": "AGPL-3",
    "website": "https://odoo-community.org/",
    'images': ['images/icon.png'],
    "depends": ["crm",
                "ascendia_base"],
    "data": ['security/ir.model.access.csv',
             'data/data.xml',
             'views/ascendia_training_credits.xml'
    ],
    "installable": True,
    "auto_install": False,
}
