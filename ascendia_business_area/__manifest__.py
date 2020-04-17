# -*- coding: utf-8 -*-
# Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Ascendia Business Area",
    "version": "10.0.1.0.0",
    "author": "Yunesky Del Rio",
    "category": "Sales",
    "license": "AGPL-3",
    "website": "https://odoo-community.org/",
    "depends": ["crm",
                "ascendia_crm",
                "sale",
                "ascendia_price_request"],
    "data": ['views/business_area_view.xml',
             'views/report_sale_order.xml'],
    "installable": True,
    "auto_install": False,
}
