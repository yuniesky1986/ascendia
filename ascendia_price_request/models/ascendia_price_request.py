from odoo import fields, models, api,_
from odoo.exceptions import ValidationError


class PriceRequest(models.Model):
    _name = 'ascendia.price.request'

    name = fields.Char(
        string="Name")
    client_id = fields.Many2one(
        'res.partner',
        string='Entity')
    responsible_id = fields.Many2one(
        'res.users',
        string='Responsible',
        default=lambda a: a.env.user)
    sale_order_ids = fields.One2many(
        'sale.order',
        'price_request_id',
        string='Sale Orders')
    purchase_order_ids = fields.One2many(
        'purchase.order',
        'price_request_id',
        string='Purchase Orders')
    purchase_state = fields.Boolean(
        compute='_get_purchase_state')
    description = fields.Text(
        string="Description")
    request_date = fields.Date(
        string="Date")
    partner_line_ids = fields.One2many(
        'ascendia.price.request.partner.line',
        'request_id')
    state = fields.Selection(
        [('draft', 'Draft'),
         ('finish', 'Finished'),
         ('canceled', 'Canceled')],
        string='State',
        readonly=True,
        default='draft')
    total_sale = fields.Float(
        compute='_compute_total_price',
        string='Total Sale Price')
    total_purchase = fields.Float(
        compute='_compute_total_price',
        string='Total Purchase Price')
    total_gain = fields.Float(
        compute='_compute_total_price',
        string='Total Gain')

    @api.one
    def _compute_total_price(self):
        total_sale = 0
        total_purchase = 0
        total_gain = 0
        for line in self.partner_line_ids:
            total_sale += line.total_sale
            total_purchase += line.total_purchase
            total_gain = line.total_gain
        self.total_sale = total_sale
        self.total_purchase = total_purchase
        self.total_gain = total_gain

    @api.one
    def _get_purchase_state(self):
        purchase_state = False
        total = 0
        for purchase in self.purchase_order_ids:
            if purchase.state not in ['draft', 'cancel']:
                total += 1
        if total and total == len(self.purchase_order_ids):
            purchase_state = True
        self.purchase_state = purchase_state

    @api.multi
    def button_dummy(self):
        return True

    @api.one
    def action_create_sale_order(self):
        if len(self.sale_order_ids):
            raise ValidationError(_('A sale order already exit link to this'))
        order_id = self.env['sale.order'].create({'partner_id':
                                                  self.client_id.id,
                                                  'price_request_id': self.id})
        for partner_line in self.partner_line_ids:
            for line in partner_line.line_ids:
                if not line.product_id:
                    prod = self.env['product.product'].create({'name':
                                                               line.name,
                                                               'type':
                                                               'service'})
                    line.product_id = prod
                values = {'product_id':
                          line.product_id and line.product_id.id or False,
                          'name': line.name,
                          'order_id': order_id.id,
                          'price_unit': line.sale_price,
                          'product_uom_qty': line.quantity}
                self.env['sale.order.line'].create(values)
        if self.sale_order_ids and self.purchase_order_ids:
            self.state = 'finish'
            self.client_id.customer = True

    @api.one
    def action_create_purchase_order(self):
        if len(self.purchase_order_ids):
            raise ValidationError(_('A purchase order already exist link to this'))
        vals = {}
        values = {}
        for partner_line in self.partner_line_ids:
            part_id = partner_line.supplier_user_id.id
            name = partner_line.display_name
            if not name:
                name = self.name + '-'
                name += partner_line.supplier_user_id.name
                partner_line.display_name = name
            if part_id not in vals:
                temp = {'partner_id': part_id,
                        'price_request_id': self.id}
                order_id = self.env['purchase.order'].create(temp).id
                vals.update({part_id: order_id})
            else:
                order_id = vals[part_id]
            for line in partner_line.line_ids:
                if line.product_id:
                    product_id = line.product_id
                else:
                    temp1 = {'name': line.name,
                             'type': 'service'}
                    product_id = self.env['product.product'].create(temp1)
                values = {'product_id': product_id.id,
                          'name': product_id.name,
                          'order_id': order_id,
                          'price_unit': line.purchase_price,
                          'product_qty': line.quantity,
                          'product_uom': product_id.uom_id.id,
                          'date_planned': self.request_date}
                self.env['purchase.order.line'].create(values)
        if self.sale_order_ids and self.purchase_order_ids:
            self.state = 'finish'

    @api.one
    def action_draft(self):
        self.state = 'draft'

    @api.one
    def action_confirm(self):
#        thread_pool = self.env['mail.thread']
        if not self.partner_line_ids:
            raise ValidationError(_('Please select at least one Line.'))
#        for partner_line in self.partner_line_ids:
#            partner = partner_line.partner_id
#            if not partner.email:
#                raise ValidationError(_('Partner %s have not email address'
#                                        % partner.name))
#            recipient_partners = list()
#            recipient_partners.append((4, partner.id))
#            url = partner_line.url
#            body = "<a href='%s'>%s</a>" % (url, _('Price Request'))
#            post_vars = {'partner_ids': recipient_partners}
#            thread_pool.message_post(body, _('Price Request'),
#                                     "notification",
#                                     "mt_comment",
#                                     **post_vars)
#            if partner.email:
#                partner_line.send_email()
        self.state = 'finish'

    @api.one
    def action_done(self):
        self.state = 'done'

    @api.one
    def action_cancel(self):
        self.check_remove_action()
        self.state = 'canceled'
        for partner_line in self.partner_line_ids:
            partner_line.state = 'draft'
        for po in self.purchase_order_ids:
            po.state = 'cancel'
        for so in self.sale_order_ids:
            so.state = 'cancel'

    @api.one
    def check_remove_action(self):
        for po in self.purchase_order_ids:
            if po.state not in ['draft', 'cancel']:
                raise ValidationError(_('You can delete or cancel a '
                                        'request with purchase orders '
                                        'in state different of draft'))

        for so in self.sale_order_ids:
            if so.state not in ['draft', 'cancel']:
                raise ValidationError(_('You can delete or cancel a '
                                        'request with sale orders '
                                        'in state different of draft'))
        return True

    @api.one
    def unlink(self):
        if self.state not in ['draft', 'canceled']:
            raise ValidationError(_('You can delete a request '
                                    'in this state '
                                    'only in draft state'))
        self.check_remove_action()
        return super(PriceRequest, self).unlink()

    @api.model
    def create(self, vals):
        name = self.env['ir.sequence'].next_by_code('price.request')
        vals.update({'name': name or '/'})
        return super(PriceRequest, self).create(vals)


class PriceRequestPartnerLine(models.Model):
    _name = 'ascendia.price.request.partner.line'
    _rec_name = 'display_name'

    request_id = fields.Many2one(
        'ascendia.price.request',
        string='Request')
    supplier_user_id = fields.Many2one(
        'res.partner',
        string='Partner')
    display_name = fields.Char(
        compute='_compute_display_name',
        store=True,
        index=True)
    url = fields.Char(
        compute='_compute_url')
    total_sale = fields.Float(
        compute='_compute_total_price',
        string='Total Sale Price')
    total_purchase = fields.Float(
        compute='_compute_total_price',
        string='Total Purchase Price')
    total_gain = fields.Float(
        compute='_compute_total_price',
        string='Total Gain')
    line_ids = fields.One2many(
        'ascendia.price.request.line',
        'request_partner_id',
        states={'done': [('readonly', True)]})
    state = fields.Selection(
        [('draft', 'Draft'),
         ('pending', 'Pending'),
         ('done', 'Done')],
        string='State',
        readonly=True,
        default='draft')
    notes = fields.Text(
        string='Notes')

    @api.one
    def action_draft(self):
        self.state = 'draft'
        for line in self.line_ids:
            line.state = 'draft'
        self.request_id.state = 'ready_to_edit'

    @api.one
    def action_pending(self):
        self.state = 'pending'
        for line in self.line_ids:
            line.state = 'pending'
#        if self.sudo().request_id.responsible_id.partner_id.email:
#            self.send_email_done()

    @api.one
    def action_done(self):
        self.state = 'done'
        for line in self.line_ids:
            line.state = 'done'
        partner_line_ids = self.search([('request_id', '=',
                                         self.request_id.id),
                                        ('state', '=', 'done')])
        if len(partner_line_ids) == len(self.request_id.partner_line_ids):
            self.request_id.action_done()

    @api.onchange('request_id', 'supplier_user_id')
    def _compute_display_name(self):
        display_name = ''
        if self.request_id:
            display_name = self.request_id.name or ' '
        if self.supplier_user_id:
            display_name += '-' + self.supplier_user_id.name
        self.display_name = display_name

    @api.one
    def _compute_url(self):
        server = self.env['ir.config_parameter'].get_param('web.base.url')
        menu = self.env['ir.model.data'].xmlid_to_res_id('ascendia_price_request.menu_price_request_partner')
        action = self.env['ir.model.data'].xmlid_to_res_id('ascendia_price_request.action_price_request_partner_line')
        url = "%s/web#id=%s&view_type=form" \
              "&model=ascendia.price.request.partner.line" \
              "&menu_id=%s&action=%s" \
              % (server, self.id, menu, action)
        self.url = url

    @api.one
    def send_email(self):
        tpl = 'ascendia_price_request.email_template_price_request'
        template = self.env.ref(tpl, False)
        if template:
            template.sudo().send_mail(self.id)

    @api.one
    def send_email_done(self):
        tpl = 'ascendia_price_request.email_template_price_request_done'
        template = self.env.ref(tpl, False)
        if template:
            template.sudo().send_mail(self.id)

    @api.one
    def _compute_total_price(self):
        total_sale = 0
        total_purchase = 0
        for line in self.line_ids:
            total_sale += line.sale_price * line.quantity
            total_purchase += line.purchase_price * line.quantity
        self.total_sale = total_sale
        self.total_purchase = total_purchase
        self.total_gain = total_sale - total_purchase


class PriceRequestLine(models.Model):
    _name = 'ascendia.price.request.line'

    name = fields.Char(
        string="Name")
    name_inf = fields.Char(
        string="Name",
        related='name')
    request_partner_id = fields.Many2one(
        'ascendia.price.request.partner.line',
        string='Partner Line')
    state = fields.Selection(
        [('draft', 'Draft'),
         ('pending', 'Pending'),
         ('done', 'Done')],
        string='State',
        readonly=True,
        default='draft')
    product_id = fields.Many2one(
        'product.product',
        string='Product')
    product_id_inf = fields.Many2one(
        'product.product',
        string='Product',
        related='product_id')
    purchase_price = fields.Float(
        string='Purchase Price')
    sale_price = fields.Float(
        string='Sale Price')
    quantity = fields.Float(
        string='Quantity')
    total_sale = fields.Float(
        string='Total Sale Price')
    total_purchase = fields.Float(
        string='Total Purchase Price')
    total_gain = fields.Float(
        string='Total Gain')

    @api.onchange('product_id')
    def onchange_product(self):
        self.name = self.product_id and self.product_id.name or ''

    @api.onchange('sale_price', 'purchase_price', 'quantity')
    def onchange_compute_total_price(self):
        self.total_sale = self.sale_price * self.quantity
        self.total_purchase = self.purchase_price * self.quantity
        self.total_gain = self.total_sale - self.total_purchase
