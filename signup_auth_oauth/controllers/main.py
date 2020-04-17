# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import logging
from odoo import http
from odoo.addons.auth_signup.controllers.main import AuthSignupHome as Home
from odoo.http import request
from odoo.tools.translate import _
import werkzeug.utils
from odoo.addons.auth_signup.models.res_users import SignupError


_logger = logging.getLogger(__name__)

# ----------------------------------------------------------
# Controller
# ----------------------------------------------------------


class OAuthLogin(Home):

    no_list_providers = False

    def list_providers(self):
        providers = super(OAuthLogin, self).list_providers()
        if self.no_list_providers:
            providers = []
        self.no_list_providers = False
        return providers

    @http.route('/web/signup', type='http', auth='public', website=True)
    def web_auth_signup(self, *args, **kw):
        self.no_list_providers = True
        response = super(OAuthLogin, self).web_auth_signup(*args, **kw)
        return response

    @http.route()
    def web_auth_reset_password(self, *args, **kw):
        qcontext = self.get_auth_signup_qcontext()
        providers = []
        qcontext.update(providers=providers)

        if not qcontext.get('token') and not qcontext.get('reset_password_enabled'):
            raise werkzeug.exceptions.NotFound()

        if 'error' not in qcontext and request.httprequest.method == 'POST':
            try:
                if qcontext.get('token'):
                    self.do_signup(qcontext)
                    return super(OAuthLogin, self).web_login(*args, **kw)
                else:
                    login = qcontext.get('login')
                    assert login, "No login provided."
                    res_users = request.registry.get('res.users')
                    res_users.reset_password(request.cr, openerp.SUPERUSER_ID, login)
                    qcontext['message'] = _("An email has been sent with credentials to reset your password")
            except SignupError:
                qcontext['error'] = _("Could not reset your password")
                _logger.exception('error when resetting password')
            except Exception, e:
                qcontext['error'] = e.message or e.name

        return request.render('auth_signup.reset_password', qcontext)
