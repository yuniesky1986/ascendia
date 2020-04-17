from odoo import fields, models, api,_
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    proposal_id = fields.Many2one(
        'ascendia.sale.proposal',
        'Contract')

    @api.one
    def _check_proposal_to_invoice(self):
        if len(self.proposal_id):
            if self.proposal_id.is_out_date or \
                            self.proposal_id.state != 'approved':
                raise ValidationError(
                    _('Contract must be approved an not out of date'))
        else:
            raise ValidationError(
                _('Order must have Contract to allow invoice'))

    @api.multi
    def action_invoice_create(self, grouped=False, final=False):
        for order in self:
            order._check_proposal_to_invoice()
        super(SaleOrder, self).action_invoice_create(grouped, final)
