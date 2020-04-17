# -*- coding: utf-8 -*-
from odoo import models, fields, api, SUPERUSER_ID, _, registry
from odoo.exceptions import AccessDenied
import json
import logging
_logger = logging.getLogger(__name__)


class SignupError(Exception):
    pass


class res_partner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def _signup_retrieve_partner(self, token, check_validity=False,
                                 raise_exception=False):
        partner_ids = self.search([('signup_token', '=', token)], limit=1)
        if not partner_ids:
            partner_ids = self.search([('signup_token', '=', token),
                                       ('active', '=', False)], limit=1)
            if not partner_ids:
                if raise_exception:
                    raise SignupError("Signup token '%s' is not valid" % token)
                return False
        if check_validity and not partner_ids.signup_valid:
            if raise_exception:
                raise SignupError("Signup token '%s' is no longer valid" % token)
            return False
        return partner_ids


class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model
    def _auth_oauth_signin(self, provider, validation, params):
        oauth_uid = validation['user_id']
        try:
            oauth_user = self.search([("oauth_uid", "=", oauth_uid),
                                      ('oauth_provider_id', '=', provider)])
            if not oauth_user:
                raise AccessDenied()
            assert len(oauth_user) == 1
            oauth_user.write({'oauth_access_token': params['access_token']})
            return oauth_user.login
        except AccessDenied, access_denied_exception:
            if self.env.context.get('no_user_creation'):
                return None
            state = json.loads(params['state'])
            token = state.get('t')
            values = self._generate_signup_values(provider, validation, params)
            email = validation.get('email',
                                   'provider_%s_user_%s' % (provider,
                                                            oauth_uid))
            oauth_user = self.search(['|',
                                      ("email", "=", email),
                                      ('login', '=', email)],
                                     limit=1)
            if oauth_user:
                oauth_user.write(values)
                return oauth_user.login
            try:
                _, login, _ = self.signup(values, token)
                return login
            except SignupError:
                raise access_denied_exception

    @classmethod
    def _login(cls, db, login, password):
        user_id = False
        with registry(db).cursor() as cr:
            try:
                cr.autocommit(True)
                # check if user exists
                env = api.Environment(cr, SUPERUSER_ID, {})
                res = env['res.users'].search(cr, SUPERUSER_ID, [('login', '=', login)],
                                              limit=1)
                if res:
                    user_id = res
                    user_id.check_credentials(cr, user_id, password)
                    try:
                        update_clause = 'NO KEY UPDATE' if cr._cnx.server_version >= 90300 else 'UPDATE'
                        cr.execute("SELECT id FROM res_users WHERE id=%%s FOR %s NOWAIT" % update_clause, (user_id,), log_exceptions=False)
                        cr.execute("UPDATE res_users SET login_date = now() AT TIME ZONE 'UTC' WHERE id=%s", (user_id,))
                        user_id.invalidate_cache(cr, user_id, ['login_date'],
                                              [user_id])
                    except Exception:
                        _logger.debug("Failed to update last_login for db:%s login:%s", db, login, exc_info=True)
            except AccessDenied:
                _logger.info("Login failed for db:%s login:%s", db, login)
                user_id = False
            finally:
                cr.close()
        return user_id

