# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    'name': 'Odoo signup auth oauth',
    'version': '8.0.0.0',
    'author': 'Yuniesky Del Rio',
    "category": "Authentication",
    'license': 'AGPL-3',
    'depends': [
        'base',
        'auth_oauth',
        'auth_signup'
    ],
    "data": ['views/auth_signup_login.xml'],
    "demo": [
    ],
    'test': [
    ],
    "installable": True
}
