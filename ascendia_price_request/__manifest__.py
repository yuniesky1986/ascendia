# -*- coding: utf-8 -*-
# Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Ascendia Price Request",
    "version": "10.0.1.0.0",
    "author": "Rembero Loanny, Yunesky Del Rio",
    "category": "Sale",
    "license": "AGPL-3",
    "website": "https://odoo-community.org/",
    "depends": ["ascendia_base",
                "product",
                "sale",
                "purchase"],
    "data": ['data/data.xml',
#             'security/security.xml',
             'security/ir.model.access.csv',
             'views/ascendia_price_request_view.xml',
             'views/sale_order_view.xml',
             'views/purchase_order_view.xml'],
    "installable": True,
    "auto_install": False,
}
