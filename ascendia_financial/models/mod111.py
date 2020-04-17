# -*- coding: utf-8 -*-
# Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api, tools, _

class L10nEsAeatMod111Report(models.Model):
    _inherit = 'l10n.es.aeat.mod111.report'
    
    @api.model
    def _get_report_line8_values(self):
        result = []
        tax_lines = self.tax_line_ids.filtered(lambda x: x.field_number in (8,))
        partners_lines = tax_lines.mapped('move_line_ids').mapped('partner_id')
        for partner in partners_lines:
            lines = tax_lines.mapped('move_line_ids').filtered(lambda x: x.partner_id.id in (partner.id,))
            base = sum(lines.mapped('debit'))
            cuota_tax_lines = self.tax_line_ids.filtered(lambda x: x.field_number in (9,)).mapped('move_line_ids').filtered(lambda x: x.partner_id.id in (partner.id,))
            cuota = sum(cuota_tax_lines.mapped('credit'))
            tax = cuota_tax_lines[0].tax_line_id.amount if cuota_tax_lines[0].tax_line_id else 0
            result.append({'partner': partner.name, 'NIF': partner.partner_nif, 'base': base, 'cuota': cuota, 'tax': abs(tax)})
        return result
