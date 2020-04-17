# -*- coding: utf-8 -*-
# Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api, tools, _

class L10nEsAeatTaxLine(models.Model):
    _inherit = 'l10n.es.aeat.tax.line'

    @api.multi
    def get_calculated_move_lines(self):
        view = self.env.ref('l10n_es_aeat.view_move_line_tree')
        return {
                'name' : _('Journal Items'),
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'account.move.line',
                'type': 'ir.actions.act_window',
                'domain': [('id', 'in', self.move_line_ids.ids)],
                'views': [(view.id, 'tree')],
        }