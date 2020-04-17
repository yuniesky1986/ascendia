# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010, 2014 Tiny SPRL (<http://tiny.be>).
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
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import csv
from openerp import models, fields, api, _
from openerp.exceptions import ValidationError
from datetime import datetime


class SyncPodio(models.TransientModel):
    _name = 'sync.podio'

    show_msg = fields.Boolean()
    msg_updated = fields.Char()
    podio_app = fields.Selection(
        [('partner', 'Partner'),
         ('contact', 'Contact'),
         ('invoice', 'Invoice'),
         ('move_line', 'Account Move Line'),
         ('project', 'Project')],
        string="Podio App",
        required=True)
    invoice_state = fields.Selection(
        [('draft', 'Draft'),
         ('open', 'Open')],
        string="Podio App")
    file = fields.Binary(
        string="Podio File",
        required=True)
    delimiter = fields.Selection(
        [(',', 'Comma'),
         (';', 'Semicolon')])

    @api.multi
    def process(self):
        rows = csv.reader(StringIO(self.file.decode('base64')),
                          quotechar='"', delimiter=str(self.delimiter),
                          dialect=csv.excel_tab)
        entries = []
        rownum = 0
        for row in rows:
            if rownum == 0:
                header = row
            elif rownum > 0:
                entry = {}
                colnum = 0
                for col in row:
                    entry[header[colnum]] = col.replace('"', '')
                    colnum += 1
                entries.append(entry)
            rownum += 1
        msg = ""
        result_cant = 0
        for entry in entries:
            if entry:
                if self.podio_app == 'partner':
                    cant, msg1 = self.process_partner(entry)[0]
                elif self.podio_app == 'contact':
                    cant, msg1 = self.process_contact(entry)[0]
                elif self.podio_app == 'invoice':
                    cant, msg1 = self.process_invoice(entry)[0]
                elif self.podio_app == 'move_line':
                    cant, msg1 = self.process_move_line(entry)[0]
                elif self.podio_app == 'project':
                    cant, msg1 = self.process_project(entry)[0]
                msg += msg1 + '<br/>'
                result_cant += cant
                self.env.cr.commit()
        self.msg_updated = str(result_cant) + '<br/>' + msg
        self.show_msg = True
        mod_obj = self.env['ir.model.data']
        res = mod_obj.get_object_reference('ascendia_podio_sync',
                                           'sync_podio_form')
        res_id = res and res[1] or False
        return {'name': _('Sync with Podio'),
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': [res_id],
                'res_model': 'sync.podio',
                'context': self.env.context.copy(),
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                'target': 'new',
                'res_id': self.id}

    @api.one
    @api.multi
    def process_contact(self, entry):
        partner = self.env['res.partner']

        vals = {'podio_cont_id': entry['podio_cont_id'],
                'name': entry['name'],
                'phone': entry['phone1'] or entry['phone2'],
                'mobile': entry['mobile'],
                'email': entry['email'],
                'function': entry['function'],
                'alternative_email': entry['alternative_email'],
                'partner_nif': entry['partner_nif'],
                'twitter': entry['twitter'],
                'linkedin': entry['linkedin'],
                'facebook': entry['facebook']}
        podio_id = entry['podio_id'].split(',')
        if podio_id:
            parent_id = partner.search([('podio_id', '=', podio_id[0])],
                                       limit=1)
            vals.update({'parent_id': parent_id.id})
        departament = entry['departament']
        if departament:
            dpto = self.env['ascendia.department']
            dpto_id = dpto.search([('name', 'in', departament.split(';'))])
            vals.update({'departament': dpto_id and dpto_id[0].id or False})
        pqd = entry['pqd']
        if pqd:
            res = ''
            if pqd == 'Si PQD':
                res = 'yes_pqd'
            elif pqd == 'No PQD':
                res = 'no_pqd'
            else:
                res = 'unknown'
            vals.update({'pqd': res})
        ascendia = entry['ascendia']
        if ascendia:
            asc = self.env['ascendia.ascendia']
            asc_id = asc.search([('name', 'in', ascendia.split(';'))])
            vals.update({'ascendia': asc_id and asc_id[0].id or False})
        partner.create(vals)
        cant = 1
        msg = entry['podio_cont_id']
        return cant, msg

    @api.one
    @api.multi
    def process_partner(self, entry):
        msg = ""
        partner = self.env['res.partner']
        act = self.env['ascendia.activity.sector']
        podio_id = entry['Podio id']
        activity = entry.get('Sector de Actividad', '')
        size = entry.get('Size', '')
        type = entry.get('Type', '')
        cant = 0
        domain = [('podio_id', '=', podio_id)]
        exist_partner = partner.search(domain, limit=1)
        flag = False
        if exist_partner:
            if activity:
                exist_act = act.search([('display_name1', '=', activity)], limit=1)
                if not exist_act:
                    exist_act = act.create({'name': activity})
                if exist_partner and exist_act:
                    flag = True
                    exist_partner.activity_sector = exist_act.id
            if size:
                flag = True
                exist_partner.size = size
            if type:
                partner_type = 'public'
                if type == 'Privada':
                    partner_type = 'private'
                flag = True
                exist_partner.partner_type = partner_type
        if flag:
            msg += podio_id
            cant += 1
        return cant, msg

    @api.one
    @api.multi
    def process_invoice(self, entry):
        cant = 0
        msg = ""
        if entry.get('Concepto') and entry.get('podio_org_id'):
            price_unit = float(str(entry.get('base1')).replace(',', '.') or 0)
            price_unit += float(str(entry.get('base2')).replace(',', '.') or 0)
            iva = entry.get('IVA', False)
            iva_id = False
            if iva and iva != '0':
                iva_id = self.env['account.tax'].search([('amount', '=', iva),
                                                         ('type_tax_use', '=',
                                                          'sale')],
                                                        limit=1)
            irpf = entry.get('IRPF', False)
            if irpf and irpf != '0':
                iva_id = self.env['account.tax'].search([('amount', '=', irpf),
                                                         ('type_tax_use', '=',
                                                          'sale')],
                                                        limit=1)
            tax_ids = []
            if iva_id:
                tax_ids = [(6, 0, iva_id.ids)]
            invoice_line = {'name': entry.get('Concepto'),
                            'price_unit': price_unit,
                            'invoice_line_tax_ids': tax_ids}
            date = ''
            if entry.get('Fecha', False):
                date_aux = entry['Fecha'].split('/')
                if date_aux and len(date_aux[2]) == 2:
                    date = str(str(int(date_aux[2]) + 2000) + '-' + str(date_aux[1]) + '-' + date_aux[0])
                else:
                    date = str(date_aux[2]) + '-' + str(date_aux[1]) + '-' + str(date_aux[0])
            vals = {'date_invoice': date,
                    'type': 'out_invoice'}
            podio_id = entry['podio_org_id'].split(',')
            if podio_id:
                partner = self.env['res.partner']
                partner_id = partner.search([('podio_id', '=', podio_id[0])],
                                            limit=1)
                vals.update({'partner_id': partner_id.id})
            inv_id = self.env['account.invoice'].create(vals)
            inv_id._onchange_partner_id()
            account_id = inv_id.journal_id.default_credit_account_id.id
            invoice_line.update({'invoice_id': inv_id.id,
                                 'account_id': account_id})
            self.env['account.invoice.line'].create(invoice_line)
            inv_id.compute_taxes()
            if self.invoice_state == 'open':
                inv_id.action_invoice_open()
            cant = 1
            msg = entry['Concepto']
        return cant, msg

    @api.one
    @api.multi
    def process_move_line(self, entry):
        cant = 0
        msg = ""
        try:
            name = entry.get('label')
            date_aux = entry['date'].split('/')
            if date_aux and len(date_aux[2]) == 2:
                date = str(str(int(date_aux[2]) + 2000) + '-' + str(date_aux[1]) + '-' + date_aux[0])
            else:
                date = str(date_aux[2]) + '-' + str(date_aux[1]) + '-' + str(date_aux[0])
            acc = self.env['account.account']
            account_id = acc.search([('code', '=', entry.get('account'))],
                                    limit=1).id
            debit = entry.get('debit')
            credit = entry.get('credit')
            if account_id:
                values = {'name': name,
                          'date': date,
                          'account_id': account_id,
                          'debit': float(str(debit).replace(',', '.')),
                          'credit': float(str(credit).replace(',', '.')),
                          'move_id': 100}
                self.env['account.move.line'].create(values)
                cant = 1
        except Exception as exc:
            print exc
        msg = entry['label']
        return cant, msg

    @api.one
    @api.multi
    def process_project(self, entry):
        cant = 0
        msg = ""
        try:
            values = {}
            if entry.get('name'):
                values.update({'name': entry.get('name')})
            if entry.get('podio_id'):
                partner = self.env['res.partner']
                podio_id = entry.get('podio_id').split(',')[0]
                partner_id = partner.search([('podio_id', '=', podio_id)],
                                            limit=1)
                values.update({'partner_id': partner_id.id})
            if entry.get('technical'):
                user = self.env['res.users']
                technical = entry.get('technical').split(';')
                user_ids = []
                for each in technical:
                    user_id = user.search([('partner_id.name', '=', each)],
                                          limit=1)
                    if user_id:
                        user_ids.append(user_id.id)
                values.update({'user_ids': [(6, 0, user_ids)]})
            if entry.get('type'):
                type_obj = self.env['project.type']
                file_type = entry.get('type').split(';')[0]
                type_id = type_obj.search([('name', '=', file_type)], limit=1)
                values.update({'project_type_id': type_id.id})
            date_aux = entry['date_start'].split('/')
            if date_aux and len(date_aux[2]) == 2:
                date_start = str(str(int(date_aux[2]) + 2000) + '-' + str(date_aux[1]) + '-' + date_aux[0])
                values.update({'start_date': date_start})
            else:
                date_start = str(date_aux[2]) + '-' + str(date_aux[1]) + '-' + str(date_aux[0])
                values.update({'start_date': date_start})

            date_end = entry['date_end'].split('/')
            if date_aux and len(date_aux[2]) == 2:
                date_end = str(str(int(date_aux[2]) + 2000) + '-' + str(date_aux[1]) + '-' + date_aux[0])
                values.update({'end_date': date_end})
            else:
                date_end = str(date_aux[2]) + '-' + str(date_aux[1]) + '-' + str(date_aux[0])
                values.update({'end_date': date_end})
            self.env['project.project'].create(values)
        except Exception as exc:
            print exc
        msg = entry.get('podio_id')
        return cant, msg
