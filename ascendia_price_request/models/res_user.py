from odoo import models, api, _


class Users(models.Model):
    _inherit = "res.users"

#    @api.model
#    def create(self, vals):
#        user = super(Users, self).create(vals)
#        md = self.env['ir.model.data']
#        rol_id = md.xmlid_to_res_id('ascendia_price_request.group_edit_own_price_request')
#        if rol_id not in user.groups_id.mapped('id'):
#            user.partner_id.supplier = False
#            user.partner_id.customer = True
#        else:
#            user.partner_id.supplier = True
#            user.partner_id.customer = False
#        return user
#
#    @api.one
#    def write(self, vals):
#        user = super(Users, self).write(vals)
#        md = self.env['ir.model.data']
#        rol_id = md.xmlid_to_res_id('ascendia_price_request.group_edit_own_price_request')
#        if rol_id not in self.groups_id.mapped('id'):
#            self.partner_id.supplier = False
#            self.partner_id.customer = True
#        else:
#            self.partner_id.supplier = True
#            self.partner_id.customer = False
#        return user
