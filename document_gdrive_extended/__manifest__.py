# -*- coding: utf-8 -*-
# Copyright 2015 be-cloud.be Jerome Sonnet <jerome.sonnet@be-cloud.be>
# Copyright 2016 Sodexis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Google Drive Attachment Extended',
    'version': '10.0.1.0.0',
    'category': 'Tools',
    'description': """
Module that allows to attach a Google Drive Document.
    """,
    'author': "Remberto Loanny",
    'license': 'AGPL-3',
    'depends': [
        'document_gdrive',
    ],
    'data': [
        'views/document_gdrive_view.xml'
    ],
    'qweb': [

    ],
    "installable": True,
}
