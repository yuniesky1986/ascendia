from odoo import models, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.multi
    def button_confirm(self):
        for order in self:
            order.partner_id.supplier = True
        return super(PurchaseOrder, self).button_confirm()
