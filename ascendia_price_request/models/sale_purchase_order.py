from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    price_request_id = fields.Many2one(
        'ascendia.price.request',
        'Price Request')

    @api.one
    def unlink(self):
        if self.price_request_id and \
                self.price_request_id.state in ['finish']:
            raise ValidationError(_('You can delete a Sale Order whit '
                                    'a request in finished state.'))
        return super(SaleOrder, self).unlink()

    @api.multi
    def action_cancel(self):
        if self.price_request_id:
            self.price_request_id.state = 'draft'
            self.price_request_id = False
        return super(SaleOrder, self).action_cancel()


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    price_request_id = fields.Many2one(
        'ascendia.price.request',
        'Price Request')

    @api.one
    def unlink(self):
        if self.price_request_id and \
                self.price_request_id.state in ['finish']:
            raise ValidationError(_('You can delete a Purchase Order whit '
                                    'a request in finished state.'))
        return super(PurchaseOrder, self).unlink()

    @api.multi
    def button_cancel(self):
        if self.price_request_id:
            self.price_request_id.state = 'draft'
            self.price_request_id = False
        return super(PurchaseOrder, self).button_cancel()
