# -*- coding: utf-8 -*-
# Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Ascendia Menu Sales Purchase",
    "version": "10.0.1.0.0",
    "author": "Yunesky Del Rio",
    "category": "Sale",
    "license": "AGPL-3",
    "website": "https://odoo-community.org/",
    "depends": ["base",
                "sale",
                "sales_team",
                "purchase",
                "account"],
    "data": ['views/sale_order_view.xml',
             'views/purchase_order_view.xml',
             'views/menu_view.xml',
             'views/delete_view.xml',
#             'views/res_partner_view.xml'
    ],
    "installable": True,
    "auto_install": False,
}
