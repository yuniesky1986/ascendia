from odoo import models, fields, api
from datetime import date

BUSINESS_AREA_LIST = [('ssi', 'SSI'),
                      ('sgc', 'SGC'),
                      ('ssf', 'SSF'),
                      ('asc', 'ASC'),
                      ('cav', 'CAV'),
                      ('sgidi', 'SGIDI'),
                      ('sge', 'SGE')]


class CRMLead(models.Model):
    _inherit = 'crm.lead'

    business_area = fields.Selection(
        BUSINESS_AREA_LIST,
        'Business Area')

    @api.one
    def action_create_price_request(self):
        res = super(CRMLead, self).action_create_price_request()
        if self.request_id and self.business_area:
            self.request_id.business_area = self.business_area
        return res


class PriceRequest(models.Model):
    _inherit = 'ascendia.price.request'

    business_area = fields.Selection(
        BUSINESS_AREA_LIST,
        'Business Area')

    @api.one
    def action_create_sale_order(self):
        res = super(PriceRequest, self).action_create_sale_order()
        if self.business_area:
            for sale in self.sale_order_ids:
                sale.business_area = self.business_area
        return res


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    business_area = fields.Selection(
        BUSINESS_AREA_LIST,
        'Business Area')


class SaleReport(models.Model):
    _inherit = "sale.report"

    business_area = fields.Selection(BUSINESS_AREA_LIST, 'Business Area',
                                     readonly=True)

    def _select(self):
        return super(SaleReport, self)._select() + \
               ", s.business_area"

    def _group_by(self):
        return super(SaleReport, self)._group_by() + ", s.business_area"
