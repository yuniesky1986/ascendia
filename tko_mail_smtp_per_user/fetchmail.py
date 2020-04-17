# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    ThinkOpen Solutions Brasil
#    Copyright (C) Thinkopen Solutions <http://www.tkobr.com>.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields , api, SUPERUSER_ID, _
import xmlrpclib
import email
import logging

_logger = logging.getLogger(__name__)


class fetchmail_server(models.Model):
    """Incoming POP/IMAP mail server account"""
    _inherit = 'fetchmail.server'

    only_replies = fields.Boolean(
        'Fetch only messages sent from Odoo',
        help='Select this box to receive only replies',
        default=False)

    # Fetch only email replies
    # use this class to filter because inheritance is not working for
    # MailThread(Abstract Class)
    # parent_id will be set only for replies
    @api.multi
    def fetch_mail(self):
        """WARNING: meant for cron usage only - will commit() after each email!"""
        context = dict(self.env.context or {})
        context['fetchmail_cron_running'] = True
        mail_thread = self.env['mail.thread']
        action_pool = self.env['ir.actions.server']
        for server in self:
            _logger.info('start checking for new emails on %s server %s',
                         server.type,
                         server.name)
            context.update({'fetchmail_server_id': server.id,
                            'server_type': server.type})
            count, failed = 0, 0
            imap_server = False
            if server.type == 'imap' and server.only_replies:
                try:
                    imap_server = server.connect()
                    imap_server.select()
                    result, data = imap_server.search(None, '(UNSEEN)')
                    for num in data[0].split():
                        result, data1 = imap_server.fetch(num, '(RFC822)')
                        # check if message is a reply, with 'parent_id' skey
                        message = data1[0][1]
                        if isinstance(message, xmlrpclib.Binary):
                            message = str(message.data)
                        # Warning: message_from_string doesn't always work correctly on unicode,
                        # we must use utf-8 strings here :-(
                        if isinstance(message, unicode):
                            message = message.encode('utf-8')
                        msg_txt = email.message_from_string(message)
                        msg = mail_thread.message_parse(msg_txt,
                                                        save_original=server.original)
                        # parent_id will be set only for replies
                        parent_id = msg.get('parent_id')
                        if parent_id:
                            imap_server.store(num, '-FLAGS', '\\Seen')
                            try:
                                res_id = mail_thread.with_context(context).sudo().message_process(server.object_id.model,
                                                                                                  data1[0][1],
                                                                                                  save_original=server.original,
                                                                                                  strip_attachments=(not server.attach))
                            except Exception:
                                _logger.info('Failed to process mail from %s server %s.',
                                             server.type,
                                             server.name,
                                             exc_info=True)
                                failed += 1
                            if res_id and server.action_id:
                                server.action_id.run({'active_id': res_id,
                                                      'active_ids': [res_id],
                                                      'active_model': context.get("thread_model", server.object_id.model)})
                            imap_server.store(num, '+FLAGS', '\\Seen')
                            self.env.cr.commit()
                            count += 1

                        else:
                            # skip with a warning
                            _logger.info('Skipped to process mail without parent_id from %s server %s.', server.type,
                                         server.name,
                                         exc_info=True)
                            # set email unseen if not copied in odoo
                            imap_server.store(num, '-FLAGS', '\Seen')
                    _logger.info("Fetched %d email(s) on %s server %s; %d succeeded, %d failed.", count,
                                 server.type,
                                 server.name, (count - failed), failed)

                except Exception:
                    _logger.info("General failure when trying to fetch mail from %s server %s.", server.type,
                                 server.name, exc_info=True)
                finally:
                    if imap_server:
                        imap_server.close()
                        imap_server.logout()
            else:
                return super(fetchmail_server, self).with_context(context).fetch_mail()
        return True
