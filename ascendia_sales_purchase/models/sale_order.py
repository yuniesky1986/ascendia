from odoo import models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_confirm(self):
        for order in self:
            order.partner_id.customer = True
        return super(SaleOrder, self).action_confirm()
