# -*- coding: utf-8 -*-
# Â© 2004-2011 Pexego Sistemas InformÃ¡ticos. (http://pexego.es)
# Â© 2012 NaNÂ·Tic  (http://www.nan-tic.com)
# Â© 2013 Acysos (http://www.acysos.com)
# Â© 2013 JoaquÃ­n Pedrosa Gutierrez (http://gutierrezweb.es)
# Â© 2014-2015 Serv. Tecnol. Avanzados - Pedro M. Baeza
#             (http://www.serviciosbaeza.com)
# Â© 2016 Antiun Ingenieria S.L. - Antonio Espinosa
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def _compute_amount_total_wo_irpf2(self):
        for invoice in self:
            # invoice.amount_total_wo_irpf = invoice.amount_tax_signed
            # for tax_line in invoice.tax_line_ids:
            #     if 'IRPF' not in tax_line.name:
            #         invoice.amount_total_wo_irpf += tax_line.amount
            invoice.amount_total_wo_irpf = invoice.amount_total

    amount_total_wo_irpf = fields.Float(
        compute="_compute_amount_total_wo_irpf2", store=True, readonly=False,
        string="Total amount without IRPF taxes")
    not_in_mod347 = fields.Boolean(
        "Not included in 347 report",
        help="If you mark this field, this invoice will not be included in "
             "any AEAT 347 model report.", default=False)
