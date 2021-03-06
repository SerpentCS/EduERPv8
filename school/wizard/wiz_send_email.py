# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
#    Copyright (C) 2011-2012 Serpent Consulting Services
#    (<http://www.serpentcs.com>)
#    Copyright (C) 2013-2014 Serpent Consulting Services
#    (<http://www.serpentcs.com>)
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

from openerp import models, fields, api


# import email
class email_template(models.Model):
    _inherit = "email.template"

    @api.multi
    def generate_email(self, template_id, res_id):
        if self._context is None:
            self._context = {}
        ret = super(email_template, self).generate_email(template_id, res_id)
        if self._context.get('body_text', False) or\
           self._context.get('subject', False) or\
           self._context.get('email_to', False):
            ret['body_text'] = self._context['body_text']
            ret['subject'] = self._context['subject']
            ret['email_to'] = self._context['email_to']
            return ret
        else:
            return ret


class send_email(models.TransientModel):
    _name = "send.email"

    note = fields.Text('Text')

    @api.multi
    def send_email(self):
        #         subject = 'Emergency mail'
        body = ''
        email_template_obj = self.env['email.template']
        template_id = email_template_obj.search([('model', '=',
                                                  'student.student')],
                                                limit=1)
        if template_id:
            for i in self:
                body += '\n' + i.note
            email_template_obj.send_mail(template_id.id,
                                         self._context.get('active_id'),
                                         force_send=True)
        return {'type': 'ir.actions.act_window_close'}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
